import sys
import json
import gspread
import numpy as np
import pandas as pd
from match_survey.utils import load_json

class Config:
    template = {
        'season_book_name': str,
        'match_book_name': str,
        'sheet_name': str,
        'raw_data_file': str,
        'index_col': list,
        'player_cols': list,
        'manager_regex': str,
        'team_perf_col': str,
        'opp_perf_col': str,
        'ref_col': str,
        'potm_col': str,
        'manager_cols': list,
        'survey_cols': list,
        'season_book_url': str,
        'creds_file': str,
        'season_cols': list,
        'fotmob_match_url': str,
        'fbref_team_url': str,
        'fbref_match_url': str,
        'description': str,
        'data_dir': str,
        'team': str
    }
    def __init__(self, config_filename: str):
        self.config_filename = config_filename
        self.config = self.load_json()
        for k,v in self.config.items():  # attributes for items in config too
            setattr(self, k, v)
        for k,v in self.template.items():  # standard typing for important attr
            try:
                setattr(self, k, v(self.config[k]))
            except:
                print(f"missing {k}")

    def load_json(self) -> dict:
        msg = f'{self.config_filename} not found'

        return load_json(self.config_filename, msg, True)

    def gather_attr(self, instance) -> dict:
        for k,v in self.__dict__.items():
            setattr(instance, k, v)