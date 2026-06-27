import os
import yaml


def config_loader(filename="config.yml", search_paths=None):
    """
    Finds a YAML file and loads it into a dictionary.

    :param filename: name of the yml file to find
    :param search_paths: list of directories to search in (default: current dir + script dir)
    :return: dict with config data
    """
    if search_paths is None:
        search_paths = [
            os.getcwd(),
            os.path.dirname(os.path.abspath(__file__)),
        ]

    for path in search_paths:
        full_path = os.path.join(path, filename)
        if os.path.isfile(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return data if data else {}

    raise FileNotFoundError(f"Could not find '{filename}' in: {search_paths}")


# Module-level singleton so other files can do: from config_loader import config
config = config_loader("config.yml")
