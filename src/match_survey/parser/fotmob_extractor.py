import re
import json
import requests
import numpy as np
import pandas as pd
from pathlib import Path
from copy import deepcopy
from bs4 import BeautifulSoup
from match_survey.connect.base_api_caller import BaseAPICaller
from match_survey.utils import get, get_all, get_path, load_defaults

class FotMobCaller(BaseAPICaller):
    def __init__(self, config_filename: str, defaults_filename: str):
        super().__init__(config_filename)
        load_defaults(defaults_filename, self)
        self.token = None
        self.raw_data_file = f'{self.data_dir}{self.match_week}_raw_fotmob.html'
        self.raw_data = str()
        self.read_data()
        self.soup = None
        self.prepare_soup()
        self.match = FotMobMatch(**self.__dict__)

    def __call__(self):
        self.call_api()
        self.save_raw_data_file()
        self.match()
        self.save()

    def get_token(self):
        pass

    def call_api(self):
        if not getattr(self.match, 'response_text', None):
            headers = {"User-Agent": "Mozilla/5.0"}
            url = getattr(self, 'fotmob_match_url', str())
            print(f'scraping {url}')
            response = requests.get(url, headers=headers)
            self.raw_data = response.text

    def save_raw_data_file(self):
        print(f'saving raw data to {self.raw_data_file}')
        if not self.raw_data:
            self.raw_data = self.match.response_text
        Path(self.raw_data_file).write_text(self.raw_data, encoding="utf-8")

    def prepare_soup(self):
        self.soup = BeautifulSoup(self.raw_data, "lxml")

    def read_data(self) -> None:
        print(f'try to read from file: {self.raw_data_file}')
        if self.raw_data:
            print('raw_data already set')
            return

        for kwargs in [{'encoding': 'utf-8'}, {}]:
            try:
                self.raw_data = Path(self.raw_data_file).read_text(**kwargs)
                if self.raw_data:
                    return
            except Exception as e:
                print(e)
        print(f'could not read from {self.raw_data_file}')


    def save(self) -> None:
        self.save_raw_data_file()
        self.match.save()


class Teams:
    def __init__(self):
        self.subs = {
            "team_index": list(),
            "name": list(),
            "label": list(),
            "sub_minute": list(),
            "sub_direction": list(),
            "rating": list()
        }

    def update_subs(self, index, name, label, minute, direction, rating):
        self.subs["team_index"].append(index)
        self.subs["name"].append(name)
        self.subs["label"].append(label)
        self.subs["sub_minute"].append(minute)
        self.subs["sub_direction"].append(direction)
        self.subs["rating"].append(rating)

    def as_df(self, team=[0,1]):
        df = pd.DataFrame(self.subs)
        return df[df.team_index.isin(team)]



class FotMobMatch:
    def __init__(self, **kwargs):
        #team=str(),
        #match_url=str(),
        #data_dir='.',
        #soup=None,
        #match_week=str(),
        #campaign=str()):
        for k,v in kwargs.items():
            setattr(self, k, v)
#        self.team = kwargs.get('team')
        self.url = kwargs['fotmob_match_url']
#        self.data_dir = data_dir')
        self.response_text = None
#        self.soup = soup')
#        self.match_week = match_week')
        self.ensure_soup()
        # main items to extract
        self.competition = kwargs.get('competition', getattr(self, 'campaign', str()))
        self.round = kwargs.get('round', getattr(self, 'round', str()))
        self.venue = str()
        self.team_is_home = True
        self.teams = Teams()
        self.lineup = pd.DataFrame()
        self.context = dict()

    def __call__(self, fotmob_name_mapping=dict()):
        self.which_venue()
        self.what_competition_round()
        self.is_team_home_or_away()
        self.get_starters_subbed()
        self.get_bench()
        self.prepare_team_lineup(fotmob_name_mapping)
        self.prepare_match_context()

    def save(self):
        lineup_filename = f'{self.data_dir}fotmob_lineup_{self.round}.csv'
        print(f'saving lineup to {lineup_filename}')
        self.lineup.to_csv(lineup_filename, index=False)
        context_filename = f'{self.data_dir}/fotmob_context_{self.round}.json'
        msg = ''
        _path = get_path(context_filename, msg, False)
        print(f'saving context to {_path}')
        _path.write_text(json.dumps(self.context))

    def prepare_match_context(self):
        self.context = {key: getattr(self, key, str()) \
            for key in ["team", "venue", "is_home", "competition", "round", "is_home"]}
        self.context["fotmob_match_url"] = self.url

    def ensure_soup(self):
        if len(self.soup)==0:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(self.url, headers=headers)

            if response.status_code != 200:
                print("Failed to retrieve page")
                return None

            self.response_text = response.text
            self.soup = BeautifulSoup(response.text, "lxml")

    def bench_label(self, group_index):
        _manager = "Manager"
        _subs = "Subs"
        _untapped = "Untapped"
        _inj_sus = "Injured/Suspended"
        match int(group_index):
            case 0 | 4:
                return _manager
            case 1 | 5:
                return _subs
            case 2 | 6:
                return _untapped
            case 3 | 7:
                return _inj_sus

    def get_starters_subbed(self):
        for starters_section in get_all(self.soup, "section", "LineupFieldContainer"):
            for i, team_div in enumerate(get_all(starters_section, "div", "TeamContainer ")):
                for player_div in get_all(team_div, "div", "PlayerDiv "):
                    name = get(player_div, "span", "LineupPlayerText ")
                    if name:
                        name = re.sub(r'^\d+', '', name.text)
                    else:
                        print("starter player name not detected")
                    rating = self.get_player_rating(player_div)
                    minute_sub = str()
                    sub_status = str()
                    for sub_div in get_all(player_div, "div", "SubInOutContainer "):
                        sub_span = get(sub_div, "span", "SubText ")
                        if sub_span:
                            minute_sub = sub_span.text.strip()
                            sub_status = "out"
                    self.teams.update_subs(i, name, "Starter", minute_sub, sub_status, rating)

    def get_bench(self):
        for group_index, bench_section in enumerate(get_all(self.soup, "section", "BenchesContainer ")):
            bench_label = self.bench_label(group_index)
            #print(group_index, bench_label)
            for team_index, bench_ul in enumerate(get_all(bench_section, "ul", "BenchContainer ")):
                #print(group_index, team_index, bench_label)
                for player_div in get_all(bench_ul, "div", "LineupPlayerCSS "):
                    name = get(player_div, "span", "LineupPlayerText ")
                    if name:
                        name = re.sub(r'^\d+', '', name.text)
                    else:
                        print("bench name not detected")
                    rating = self.get_player_rating(player_div)
                    #print(group_index, team_index, bench_label, name)
                    #if bench_label == 'Manager':
                    #    print(group_index, name, bench_label)
                    minute_sub = str()
                    sub_status = str()
                    if sub_details := get_all(player_div, "div", "SubInOutContainer "):
                        for sub_div in sub_details:
                            sub_span = get(sub_div, "span", "SubText ")
                            if sub_span:
                                #print('is sub')
                                minute_sub = sub_span.text.strip()
                                sub_status = "in"
                    self.teams.update_subs(team_index, name, bench_label, minute_sub, sub_status, rating)

    def prepare_team_lineup(self, roster_surname_mapping=dict()):
        team_lineup = self.teams.as_df()
        team_filter = 0 if self.is_home else 1
        team_lineup = team_lineup[team_lineup['team_index']==team_filter]
        team_lineup.loc[:, 'name'] = team_lineup['name'] \
            .apply(lambda x: roster_surname_mapping.get(x, x))
        team_lineup.rename(columns={'name': 'player'}, inplace=True)

        self.lineup = team_lineup.reset_index(drop=True)

    def is_team_home_or_away(self):
        team_containers = get_all(self.soup, "div", "TeamMarkup")
        for i, cntnr in enumerate(team_containers):
            self.is_home = i % 2 == 0
            tname = get(cntnr, 'span', 'TeamNameItself')
            if self.team in tname.text:
                break

    def which_venue(self):
        venue_a = get(self.soup, "a", "VenueCSS ")
        if not venue_a:
            print('could not find Venue "a"')
            self.venue = str()
            return

        venue_span = venue_a.find('span')
        if not venue_span:
            print('could not find Venue "span"')

        self.venue = venue_span.text

    def what_competition_round(self):
        competition_round = get(self.soup, "span", "TournamentTitle ").text
        comp_parts = competition_round.split(' Round ')
        if len(comp_parts) == 2:
            self.competition, self.round = comp_parts
        else:
            campaign_detail = get(self.soup, "div", "MiddleGridItem")
            competition_round = campaign_detail.find("span").text
            if len(comp_parts) == 2:
                self.competition, self.round = comp_parts

        try:
            assert self.competition, 'no competition extracted'
        except AssertionError as ae:
            print(ae)
            self.competition = self.campaign

        try:
            assert self.round, 'no round extracted'
        except AssertionError as ae:
            print(ae)
            self.round = self.match_week

    def get_player_rating(self, player_div) -> float:
        rating = np.nan
        try:
            rating_ = get(player_div, "div", "PlayerRating")
            rating = rating_.find("span").text
        except:
            print('could not get rating')

        return rating

