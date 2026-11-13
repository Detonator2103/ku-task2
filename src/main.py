import argparse
import sys

from apt import AptError, get_dependencies, parse_packages, read_index
from config import ConfigError, load_config, validate_config

EXIT_OK = 0
EXIT_ERROR = 1


def parse_args():
    parser = argparse.ArgumentParser(description="Граф зависимостей пакета")
    parser.add_argument("config", help="путь к YAML-конфигурации")
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        config = load_config(args.config)
        validate_config(config)
        text = read_index(config["repository_url"], config["test_mode"])
        packages = parse_packages(text)
        deps = get_dependencies(config["package_name"], packages)
    except (ConfigError, AptError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return EXIT_ERROR
    print(f"Прямые зависимости пакета {config['package_name']}:")
    for dep in deps:
        print(f"  {dep}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())