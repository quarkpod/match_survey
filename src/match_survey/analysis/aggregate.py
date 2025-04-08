import sys
import numpy as np
import pandas as pd
from match_survey.payload.base_payload import Config

class Analyses:
    '''
    analyse responses and create survey pool results for a match

    attributes expected from Config
    - roster
    '''
    def __init__(self, responses_df: pd.DataFrame, config_filename: str):
        self.df = responses_df
        Config(config_filenmae).gather_attr(self)
        self.ratings = None

    def prepare(self) -> None:
        '''
        find player cols
        clean them (remove r'\(.*\)')
        separate numerical ratings from string fields
        '''
        self.clean_cols()
        self.find_player_cols()

    def clean_cols(self) -> None:
        #self.df = self.df.map(lambda x: None if x=='' else x)
        for col in self.df.columns:
            try:
                self.df[col] = pd.to_numeric(self.df[col])
            except:
                print(f'[{col}] treated as non-numeric columns')

    def clean_headers(self) -> None:
        self.raw_cols = self.df.columns.tolist()
        self.df.columns = [re.sub(r'\s*\(.*\)', '', x) for x in self.df.columns]

    def find_player_cols(self)
        for player in self.roster:  # roster provided by Config attr
            self.player_cols = [x for x in self.df.columns if player in x]
            
    def separate(self) -> None:
        self.num_df = self.df[[x for x in self.df.columns \
            if self.df[x].dtype == float]]
        self.str_df = self.df.loc[:, ~self.df.columns.isin(self.num_df.columns)]

    def prepare_potm(self) -> None:
        def count_potm(x, potmc):
            for y in x:
                if y not in potmc.keys():
                    if pd.isnull(y) or y in [None, '']:
                        y = 'No One'
                    potmc[y] = 0
                potmc[y] += 1
        potm_dict = {x: 0 for x in self.roster}
        _ = self.str_df.iloc[:, 0].str.split(',') \
            .apply(lambda x: count_potm(x, potm_dict))
        self.potm_srs = pd.Series(self.potm_dict).sort_values(ascending=False)

    def potm_percent(self, top_n: int=None) -> pd.Series:
        n = self.potm_srs.size
        if int(top_n) and top_n:
            n = int(top_n)
        return self.potm_srs.divide(self.potm_srs.sum()).iloc[:n]