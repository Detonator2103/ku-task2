from apt import make_apt_provider, parse_packages, read_index
from graph_file import read_graph_file


def make_provider(config):
    location = config["repository_url"]
    if config["test_mode"]:
        return read_graph_file(location).get
    text = read_index(location, False)
    return make_apt_provider(parse_packages(text))