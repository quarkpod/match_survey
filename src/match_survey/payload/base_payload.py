import sys
import json
import gspread
import numpy as np
import pandas as pd
from match_survey.utils import load_json, save_json

class Config:
    template = {
        'data_dir': str
    }
    def __init__(self, config_filename: str):
        self.config_filename = config_filename
        self.config = self.load_json()
        for k,v in self.config.items():  # attributes for items in config too
            setattr(self, k, v)
        for k,v in self.template.items():  # standard typing for important attr
            if val := self.config.get(k, None):
                setattr(self, k, v(val))

    def load_json(self) -> dict:
        msg = f'{self.config_filename} not found'

        return load_json(self.config_filename, msg, True)

    def gather_attr(self, instance) -> dict:
        for k,v in self.__dict__.items():
            setattr(instance, k, v)

    def save_json(self, filename=None):
        msg = f'trouble saving config at {filename}'
        save_json(filename, msg, True, self.config)
