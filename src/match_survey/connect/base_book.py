import sys
import json
import gspread
import numpy as np
import pandas as pd
from match_survey.payload.base_payload import Config

class BaseBook:
    def __init__(self, config_filename: str):
        Config(config_filename).gather_attr(self)
        self.book_strs = list()  # google sheet name or url
        self.client = None  # google sheet client
        self.authenticate()

    def authenticate(self) -> None:
        self.client = gspread.oauth(credentials_filename=self.creds_file)

    def read_sheet(self):
        sheet_name = getattr(self, 'sheet_name')
        self.sheet = self.book.worksheet(sheet_name)

    def connect(self):
        '''
        connects by book name or url, depending on what is given in config
        book_strs is a class attribute with book name and url keys from config
        eg,
          ['match_book_name', 'match_book_url']  <- for single matches
          ['season_book_name', 'season_book_url']  <- for analyses of season
        '''
        for _book_str in self.book_strs:
            book_str = getattr(self, _book_str, str())
            if book_str:
                self.book = self.client.open(book_str)
        if self.book is None:
            msg = f'missing {self.book_strs} in config. ' \
                + 'need at least one specified'
            sys.exit(msg)
