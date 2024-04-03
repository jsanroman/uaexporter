import pytest
from unittest.mock import mock_open, patch
from utils import load_yml

@pytest.fixture
def mock_yaml_data():
    return {
        "key": "value",
        "list": [1, 2, 3]
    }

@pytest.fixture
def mock_file_content(mock_yaml_data):
    import yaml
    return yaml.dump(mock_yaml_data)

def test_load_yml(mock_file_content, mock_yaml_data):
    # Mock open function and the yaml.safe_load
    with patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file, \
         patch("yaml.safe_load", return_value=mock_yaml_data) as mock_safe_load:
        result = load_yml("dummy")
        mock_file.assert_called_once_with("dummy.yml", 'r')
        assert result == mock_yaml_data, "The loaded YAML data did not match the expected result"
