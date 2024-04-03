import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from tqdm import tqdm
from dotenv import load_dotenv
from importlib import import_module
from connectors.connector_factory import ConnectorFactory
from report import Report
from utils import load_yml

def export():
    load_dotenv()
    config_reports = load_yml('reports')

    for config_report in tqdm(config_reports, desc='Processing reports'):
        try:
            connector = ConnectorFactory.get_connector(config_report['connector'])
        except ValueError as e:
            print(e)

        report = Report(config_report)
        connector.create_storage(report.get_storage_name(), report.get_headers())

        for page in tqdm(range(1, report.pages + 1), desc=f'Processing pages for {config_report["name"]}'):
            report.load_data(page)
            connector.insert_data(report.get_storage_name(), report.get_headers(), report.get_rows())