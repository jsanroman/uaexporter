import os
import socket

import time
import googleapiclient.discovery
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

def retry_with_backoff(func):
    """Decorator to retry a function call with exponential backoff."""
    def wrapper(*args, **kwargs):
        retries = 5  # Total number of attempts
        wait = 1  # Initial wait time between retries in seconds
        for i in range(retries):
            try:
                return func(*args, **kwargs)
            except HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:
                    # Retry on server errors
                    print(f"Retry {i+1}/{retries} after error: {e}, waiting {wait}s...")
                    time.sleep(wait)
                    wait *= 2  # Exponential backoff
                else:
                    raise  # Do not retry on client errors
            except TimeoutError as e:
                # Retry on timeout
                if i < retries - 1:
                    print(f"Retry {i+1}/{retries} after timeout: {e}, waiting {wait}s...")
                    time.sleep(wait)
                    wait *= 2
                else:
                    raise
    return wrapper

class UaConnector:
    def __init__(self):
        super().__init__()
        self.service = self._get_service()

    def _get_service(self):
        socket.setdefaulttimeout(180)

        api_name = 'analytics'
        api_version = 'v3'
        service_account_file = os.getenv('GA_SECRETS_PATH')

        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=['https://www.googleapis.com/auth/analytics.readonly'])

        return googleapiclient.discovery.build(api_name, api_version, credentials=credentials)

    @retry_with_backoff
    def get_data(self, config, start_date, end_date, start_index=1, max_results=1):
        return self.service.data().ga().get(
            ids='ga:' + os.getenv('GA_PROFILE_ID'),
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            metrics=config['metrics'],
            dimensions=config['dimensions'],
            start_index=start_index,
            max_results=max_results
        ).execute()
