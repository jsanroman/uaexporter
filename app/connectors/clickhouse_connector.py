from .base_connector import BaseConnector
import os
import clickhouse_driver

class ClickhouseConnector(BaseConnector):
    def __init__(self):
        super().__init__()
        self.client = self._get_client()

    def insert_data(self, storage_name, headers, rows):
        insert_statement = f"INSERT INTO {storage_name} VALUES"
        self.client.execute(insert_statement, self._convert_row_values(headers, rows))

    def create_storage(self, storage_name, headers):
        columns = [f"{header['name'].replace('ga:', '')} {self._convert_data_type(header['dataType'])}" for header in headers]
        create_table_statement = f"CREATE TABLE IF NOT EXISTS {storage_name} ({', '.join(columns)}) ENGINE = MergeTree() ORDER BY tuple()"
        self.client.execute(create_table_statement)

    def _convert_row_values(self, headers, rows):
        type_map = {
            'STRING': str,
            'INTEGER': int,
            'PERCENT': float,
            'TIME': float,
            'CURRENCY': float,
            'FLOAT': float,
        }
        column_data_types = [type_map[header['dataType']] for header in headers]
        converted_rows = []
        for row in rows:
            converted_row = [column_data_types[i](value) if value not in ('', None) else None for i, value in enumerate(row)]
            converted_rows.append(converted_row)
        return converted_rows

    def _convert_data_type(self, data_type):
        mapping = {
            "STRING": "String",
            "INTEGER": "Int64",
            "PERCENT": "Float64",
            "TIME": "Float64",
            "CURRENCY": "Float64",
            "FLOAT": "Float64"
        }
        return mapping.get(data_type, "String")

    def _get_client(self):
        host = os.getenv('CLICKHOUSE_HOST', 'localhost')
        port = int(os.getenv('CLICKHOUSE_PORT', '9000'))
        password = os.getenv('CLICKHOUSE_PASSWORD', '')
        database = os.getenv('CLICKHOUSE_DATABASE', 'uaexporter')

        return clickhouse_driver.Client(host=host, port=port, password=password, database=database)
