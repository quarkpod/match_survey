import sys
import json
import gspread
import numpy as np
import pandas as pd
from match_survey.payload.base_payload import Config

class BaseAPICaller:
    #book_strs = list()  # to be set in child classes, google sheet name or url
    def __init__(self, config_filename: str):
        Config(config_filename).gather_attr(self)
        self.endpoint = str()
        self.token = None
        self.raw_data = list()
        self.df = pd.DataFrame()
        self.raw_data_file = str()

    def __call__(self, save=False) -> pd.DataFrame:
        self.get_token()
        self.call_api()
        self.save_raw_data()
        #self.set_df(save)

        #return self.df

    def get_token(self) -> None:
        raise NotYetImplemented

    def call_api(self) -> None:
        raise NotYetImplemented

    def save_raw_data(self):
        raise NotYetImplemented
