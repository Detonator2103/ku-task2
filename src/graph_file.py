import re

from graph import GraphError

LINE_PATTERN = re.compile(r"^([A-Z]+)\s*:\s*([A-Z\s]*)$")


def parse_graph_text(text):
    graph = {}
    for number, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        match = LINE_PATTERN.match(line)
        if not match:
            raise GraphError(f"строка {number}: некорректный формат: {line!r}")
        name = match.group(1)
        if name in graph:
            raise GraphError(f"строка {number}: повторное описание {name}")
        graph[name] = list(dict.fromkeys(match.group(2).split()))
    return graph


def read_graph_file(path):
    try:
        with open(path, encoding="utf-8") as file:
            text = file.read()
    except (OSError, UnicodeDecodeError) as error:
        raise GraphError(f"не удалось прочитать файл графа: {error}")
    return parse_graph_text(text)