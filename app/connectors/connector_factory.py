from importlib import import_module

class ConnectorFactory:
    @staticmethod
    def get_connector(connector_name):
        try:
            module_path = f"connectors.{connector_name}_connector"

            connector_module = import_module(module_path)
        except ImportError as e:
            raise ValueError(f"Module for connector '{connector_name}' not found.") from e

        class_name = connector_name.capitalize() + 'Connector'
        try:
            connector_class = getattr(connector_module, class_name)
        except AttributeError as e:
            raise ValueError(f"Unsupported connector class: {class_name}") from e

        return connector_class()
