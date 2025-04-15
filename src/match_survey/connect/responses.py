import sys
import json
import gspread
import numpy as np
import pandas as pd
from match_survey.connect.base_book import BaseBook

class Responses(BaseBook):
    defaults = {  # defaults given by Google Sheets
        'index_col': 'Timestamp'
    }
    def __init__(self, config_filename: str):
        super().__init__(config_filename)
        self.book = None
        self.sheet = None
        self.raw_data = list()
        self.df = pd.DataFrame()
        self.raw_data_file = str()
        self.book_strs = ['match_book_name', 'match_book_url']

    def __call__(self, save=False) -> pd.DataFrame:
        self.connect()
        self.read_sheet()
        self.read_data()
        self.set_df(save)

        return self.df

    def read_data(self):
        self.raw_data = self.sheet.get_all_values()

    def set_df(self, save=False):
        index_col = getattr(self, 'index_col', self.defaults['index_col'])
        # first element is list of column names; the rest is the poll data
        self.df = pd.DataFrame(self.raw_data[1:], columns=self.raw_data[0])
        # use response Timestamp as the index for convenience
        self.df.set_index(index_col, inplace=True)
        if save:
            self.save_raw_data()

    def save_raw_data(self):
        self.df.to_csv(self.raw_data_file)
