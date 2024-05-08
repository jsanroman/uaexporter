import os
import math
import re
import datetime
from ua_connector import UaConnector

class Report:
    def __init__(self, config):
        super().__init__()
        self.ua_connector = UaConnector()
        self.config = config
        self.data = {}
        self.current_page = 0
        self.current_start_date = datetime.datetime.strptime(self.config['start_date'], "%Y-%m-%d").date()
        self.current_end_date = datetime.datetime.strptime(self.config['end_date'], "%Y-%m-%d").date()
        self.pages = 0
        self.max_results = int(os.getenv('GA_MAX_RESULTS_BY_REQUEST', 10000))

    def get_end_date(self):
        return datetime.datetime.strptime(self.config['end_date'], "%Y-%m-%d").date()

    def set_current_start_date(self, current_start_date):
        self.current_start_date = current_start_date

    def set_current_end_date(self, current_end_date):
        self.current_end_date = current_end_date

    def get_headers(self):
        return self.data["columnHeaders"]

    def get_rows(self):
        return self.data["rows"]

    def get_name(self):
        return self.config['name']

    def get_storage_name(self):
      pattern_disallowed_chars = re.compile(r'[^\w\s-]')  # Allow hyphens here to replace them later
      pattern_spaces_hyphens_underscores = re.compile(r'[\s_-]+')  # Match spaces, hyphens, and underscores
      pattern_leading_trailing_underscores = re.compile(r'^_+|_+$')

      s = self.get_name().lower().strip()
      s = pattern_disallowed_chars.sub('', s)
      s = pattern_spaces_hyphens_underscores.sub('_', s)
      s = pattern_leading_trailing_underscores.sub('', s)

      return s

    def load_data(self, page, start_date=None, end_date=None):
        self.current_page = page

        self.data = self.ua_connector.get_data(
          self.config,
          self.current_start_date, 
          self.current_end_date,
          start_index=self._start_index(), 
          max_results=self.max_results
        )

    def _start_index(self):
        return (self.current_page - 1) * self.max_results + 1

    def refresh_pagination(self):
        self.data = self.ua_connector.get_data(self.config, self.current_start_date, self.current_end_date)
        self.pages = math.ceil(self.data["totalResults"] / self.max_results)
