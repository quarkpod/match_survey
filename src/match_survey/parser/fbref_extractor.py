import sys
import json
import pickle
import requests
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from match_survey.connect.base_api_caller import BaseAPICaller

class FBRefCaller(BaseAPICaller):
    #defaults = {  # defaults given by Google Sheets
        #'index_col': 'Timestamp'
    #}
    def __init__(self, config_filename: str):
        super().__init__(config_filename)
        self.endpoint = self.fbref_team_url  # from config file
        self.token = None
        self.raw_data = list()
        #self.df = pd.DataFrame()
        self.raw_data_file = Path(self.data_dir, 'fbref_season_stats.pkl')
        self.book_strs = ['match_book_name', 'match_book_url']

    def get_token(self):
        pass  # no token needed for FBRef

    def call_api(self):
        self.raw_data = pd.read_html(self.endpoint)

    @property
    def player_season_stat_types(self):

        return ['Profile' if 'Unnamed: ' in x[0] else x[0] for x in self.raw_data[0].columns]

    @property
    def player_season_stat_columns_cleaned(self):

        return [x[1]+'/90min' if x[0]=='Per 90 Minutes' else x[1] for x in self.raw_data[0].columns]

    @property
    def player_season_stats(self):
        df = self.raw_data[0].copy(deep=True)
        df.columns = self.player_season_stat_columns_cleaned
        df.loc[:, 'Surname'] = self.player_surnames(df['Player'])

        return df

    def get_roster(self):
        players = self.player_season_stats
        subset_cols = ['Surname', 'Player', 'Pos', 'Starts', 'Min']
        roster = players[subset_cols]
        roster.fillna({'Player': '-', 'Pos': '-', 'Starts': 0, 'Min': 0}, inplace=True)
        roster = roster[~roster['Player'].str.contains('Total')]  # drops squad & opp totals
        roster.loc[:, 'Player'] = roster['Player'].apply(lambda x: self.name_mapping.get(x,x))
        roster.sort_values('Player', ascending=True, inplace=True)
        for pos in ['GK', 'DF', 'MF', 'FW']:
            roster.loc[:, pos] = roster['Pos'].str.contains(pos)

        return roster

    def set_df(self, save=False):
        index_col = getattr(self, 'index_col', self.defaults['index_col'])
        # first element are column names; the rest is the poll data
        self.df = pd.DataFrame(self.raw_data[1:], columns=self.raw_data[0])
        # use response Timestamp as the index for convenience
        self.df.set_index(index_col, inplace=True)
        if save:
            self.save_raw_data()

    def save_raw_data(self):
        with self.raw_data_file.open('wb') as outp:
            pickle.dump(self.raw_data, outp, pickle.HIGHEST_PROTOCOL)

    def load_raw_data(self):
        self.raw_data = list()
        with self.raw_data_file.open('rb') as inp:
            self.raw_data = pickle.load(inp)

    @property
    def schedule(self):

        return self.raw_data[1]

    def get_match_details(self) -> pd.Series:
        competition = self.campaign['Comp']
        comp_round = self.campaign['Round']
        match_week = self.campaign['index']

        return self.schedule[ \
            (self.schedule['Comp']==competition) & \
            (self.schedule['Round']==comp_round)
        ].iloc[match_week, :]

    def get_match_date(self, date_format='%y%m%d') -> str:
        match_date = self.get_match_details().loc['Date']  # has format like: YYYY-MM-DD

        return datetime.strptime(match_date, '%Y-%m-%d').strftime(date_format)

    @staticmethod
    def player_surnames(name_srs: pd.Series):
        """
        assumed that name_srs is like the 'Player' column from property raw_data[0] table
        """

        return name_srs.apply(lambda x: x.split(' ')[-1])

