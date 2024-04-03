import os

import googleapiclient.discovery
from google.oauth2 import service_account

class UaConnector:
    def __init__(self):
        super().__init__()
        self.service = self._get_service()

    def _get_service(self):
        api_name = 'analytics'
        api_version = 'v3'
        service_account_file = os.getenv('GA_SECRETS_PATH')

        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=['https://www.googleapis.com/auth/analytics.readonly'])

        return googleapiclient.discovery.build(api_name, api_version, credentials=credentials)

    def get_data(self, config, start_index=1, max_results=1):
        return self.service.data().ga().get(
            ids='ga:' + os.getenv('GA_PROFILE_ID'),
            start_date=config['start_date'],
            end_date=config['end_date'],
            metrics=config['metrics'],
            dimensions=config['dimensions'],
            start_index=start_index,
            max_results=max_results
        ).execute()
