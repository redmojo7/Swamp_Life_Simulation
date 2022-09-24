import yaml

CONFIG_YAML = "config/config.yml"
CREATURES_CSV = 'output/creatures.csv'


def load_config():
    with open(CONFIG_YAML, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config
