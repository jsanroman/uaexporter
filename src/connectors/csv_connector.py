from .base_connector import BaseConnector
import os
import csv

class CsvConnector(BaseConnector):
    def __init__(self):
        super().__init__()

    def insert_data(self, storage_name, headers, rows):
        with open(self._csv_path(storage_name), 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in rows:
                writer.writerow(row)

    def create_storage(self, storage_name, headers):
        file_exists = os.path.isfile(self._csv_path(storage_name))
        with open(self._csv_path(storage_name), 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                _headers = [header['name'] for header in headers]
                writer.writerow(_headers)

    def _csv_path(self, storage_name):
      return os.path.join(os.getenv('CSV_PATH', '.'), f"{storage_name}.csv")
