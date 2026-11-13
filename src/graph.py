from collections import deque


class GraphError(Exception):
    pass


def build_graph(start, provider):
    if provider(start) is None:
        raise GraphError(f"пакет не найден в репозитории: {start}")
    graph = {}
    visited = {start}
    queue = deque([start])
    while queue:
        name = queue.popleft()
        deps = provider(name) or []
        graph[name] = deps
        for dep in deps:
            if dep not in visited:
                visited.add(dep)
                queue.append(dep)
    return graph


def restore_path(parents, last, node):
    names = []
    current = last
    while current != node:
        names.append(current)
        current = parents[current]
    names.reverse()
    return [node] + names + [node]


def find_cycle(graph, node):
    parents = {}
    queue = deque()
    for dep in graph.get(node, []):
        if dep == node:
            return [node, node]
        if dep not in parents:
            parents[dep] = node
            queue.append(dep)
    while queue:
        current = queue.popleft()
        for dep in graph.get(current, []):
            if dep == node:
                return restore_path(parents, current, node)
            if dep not in parents:
                parents[dep] = current
                queue.append(dep)
    return None


def find_cycles(graph):
    cycles = []
    seen = set()
    for node in sorted(graph):
        cycle = find_cycle(graph, node)
        if cycle is not None and frozenset(cycle) not in seen:
            seen.add(frozenset(cycle))
            cycles.append(cycle)
    return cycles