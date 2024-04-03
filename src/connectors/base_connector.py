class BaseConnector:
    def __init__(self):
        pass

    def create_storage(self, storage_name, headers):
        raise NotImplementedError("Subclasses must implement this method")

    def insert_data(self, storage_name, headers, rows):
        raise NotImplementedError("Subclasses must implement this method")
