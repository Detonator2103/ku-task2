import argparse
import sys

from apt import AptError
from config import ConfigError, load_config, validate_config
from graph import GraphError, build_graph, find_cycles
from repository import make_provider

EXIT_OK = 0
EXIT_ERROR = 1
NO_DEPENDENCIES = "(нет зависимостей)"

def parse_args():
    parser = argparse.ArgumentParser(description="Граф зависимостей пакета")
    parser.add_argument("config", help="путь к YAML-конфигурации")
    return parser.parse_args()


def print_graph(name, graph):
    print(f"Граф зависимостей пакета {name} (обход BFS):")
    for package, deps in graph.items():
        text = " ".join(deps) if deps else NO_DEPENDENCIES
        print(f"  {package}: {text}")
    print(f"Всего пакетов в графе: {len(graph)}")


def print_cycles(cycles):
    if not cycles:
        print("Циклические зависимости не найдены.")
        return
    print("Найдены циклические зависимости:")
    for cycle in cycles:
        print("  " + " -> ".join(cycle))


def main():
    args = parse_args()
    try:
        config = load_config(args.config)
        validate_config(config)
        provider = make_provider(config)
        graph = build_graph(config["package_name"], provider)
    except (ConfigError, AptError, GraphError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return EXIT_ERROR
    print_graph(config["package_name"], graph)
    print_cycles(find_cycles(graph))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())