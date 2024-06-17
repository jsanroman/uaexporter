import sys
import os
import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from tqdm import tqdm
from dotenv import load_dotenv
from importlib import import_module
from connectors.connector_factory import ConnectorFactory
from report import Report
from utils import load_yml


def _get_last_day_of_month(date):
    next_month = date.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

def _get_first_day_of_next_month(date):
    if date.month == 12:
        return datetime.date(date.year + 1, 1, 1)
    else:
        return datetime.date(date.year, date.month + 1, 1)


def _generate_date_ranges(start_date, end_date, split_type):
    if not split_type:
        return [(start_date, end_date)]  # Return the entire range if split_type is blank or None

    ranges = []
    current_date = start_date
    while current_date <= end_date:
        if split_type == 'day':
            next_date = current_date + datetime.timedelta(days=1)
            ranges.append((current_date, current_date))
        elif split_type == 'month':
            last_day = _get_last_day_of_month(current_date)
            ranges.append((current_date, last_day))
            next_date = _get_first_day_of_next_month(current_date)

        current_date = next_date
    return ranges

def _import_data_for_date_range(report, connector, start_date, end_date):
    report.refresh_pagination(start_date, end_date)
    connector.create_storage(report.get_storage_name(), report.get_headers())

    for page in tqdm(range(1, report.pages + 1), desc=f'Processing pages for {report.config["name"]}'):
        report.load_data(page, start_date, end_date)
        connector.insert_data(report.get_storage_name(), report.get_headers(), report.get_rows())

def _process_reports(config_reports):
    for config_report in tqdm(config_reports, desc='Processing reports'):
        connector = ConnectorFactory.get_connector(config_report['connector'])
        report = Report(config_report)
        date_ranges = _generate_date_ranges(report.get_start_date(), report.get_end_date(), report.config.get('split_requests_by', ''))

        for start_date, end_date in date_ranges:
            _import_data_for_date_range(report, connector, start_date, end_date)

def export():
    load_dotenv()
    config_reports = load_yml('reports')
    _process_reports(config_reports)
