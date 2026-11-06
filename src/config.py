import os
import re
import yaml

REQUIRED_KEYS = [
    "package_name",
    "repository_url",
    "test_mode",
    "output_file",
]
IMAGE_EXTENSIONS = (".png", ".svg", ".jpg")
URL_PREFIXES = ("http://", "https://")
PACKAGE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9+.\-]+$")


class ConfigError(Exception):
    pass

def load_config(path):
    if not os.path.isfile(path):
        raise ConfigError(f"файл конфигурации не найден: {path}")
    try:
        with open(path, encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as error:
        raise ConfigError(f"некорректный YAML: {error}")
    if not isinstance(data, dict):
        raise ConfigError("конфигурация должна быть словарём ключ: значение")
    return data


def check_package_name(config):
    name = config["package_name"]
    if not isinstance(name, str) or not PACKAGE_PATTERN.match(name):
        raise ConfigError(f"некорректное имя пакета: {name!r}")


def check_test_mode(config):
    if not isinstance(config["test_mode"], bool):
        raise ConfigError("test_mode должен быть true или false")


def check_repository(config):
    location = config["repository_url"]
    if not isinstance(location, str) or not location:
        raise ConfigError("repository_url должен быть непустой строкой")
    if config["test_mode"]:
        if not os.path.isfile(location):
            raise ConfigError(f"тестовый файл не найден: {location}")
    elif not location.startswith(URL_PREFIXES):
        raise ConfigError("URL должен начинаться с http:// или https://")


def check_output_file(config):
    name = config["output_file"]
    if not isinstance(name, str) or not name:
        raise ConfigError("output_file должен быть непустой строкой")
    extension = os.path.splitext(name)[1].lower()
    if extension not in IMAGE_EXTENSIONS:
        raise ConfigError(f"расширение должно быть одним из {IMAGE_EXTENSIONS}")
    folder = os.path.dirname(name) or "."
    if not os.path.isdir(folder):
        raise ConfigError(f"папка не существует: {folder}")


def validate_config(config):
    for key in REQUIRED_KEYS:
        if key not in config:
            raise ConfigError(f"отсутствует параметр: {key}")
    check_package_name(config)
    check_test_mode(config)
    check_repository(config)
    check_output_file(config)