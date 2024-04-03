import yaml

def load_yml(file):
    with open(f"{file}.yml", 'r') as file:
        data = yaml.safe_load(file)
    return data
