import argparse
import sys

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
    except ConfigError as error:
        print(f"Ошибка конфигурации: {error}", file=sys.stderr)
        return EXIT_ERROR
    for key, value in config.items():
        print(f"{key}: {value}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())