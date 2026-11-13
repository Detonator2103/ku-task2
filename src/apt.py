import gzip
import lzma
import urllib.request

TIMEOUT_SECONDS = 30
DEPENDENCY_FIELDS = ("Pre-Depends", "Depends")


class AptError(Exception):
    pass

def read_bytes(location, test_mode):
    if test_mode:
        with open(location, "rb") as file:
            return file.read()
    with urllib.request.urlopen(location, timeout=TIMEOUT_SECONDS) as reply:
        return reply.read()


def decompress(data, location):
    if location.endswith(".gz"):
        return gzip.decompress(data)
    if location.endswith(".xz"):
        return lzma.decompress(data)
    return data


def read_index(location, test_mode):
    try:
        raw = read_bytes(location, test_mode)
        data = decompress(raw, location)
    except (OSError, EOFError, lzma.LZMAError) as error:
        raise AptError(f"не удалось прочитать репозиторий: {error}")
    return data.decode("utf-8", errors="replace")


def parse_block(block):
    fields = {}
    key = None
    for line in block.splitlines():
        if line.startswith((" ", "\t")):
            if key:
                fields[key] += " " + line.strip()
        elif ":" in line:
            key, _, value = line.partition(":")
            fields[key] = value.strip()
    return fields


def parse_packages(text):
    packages = {}
    for block in text.split("\n\n"):
        fields = parse_block(block)
        name = fields.get("Package")
        if name:
            packages[name] = fields
    return packages


def clean_name(text):
    name = text.split("(")[0].split("[")[0].split("<")[0].strip()
    return name.split(":")[0]


def parse_depends(value):
    names = []
    for group in value.split(","):
        name = clean_name(group.split("|")[0])
        if name:
            names.append(name)
    return names


def get_dependencies(name, packages):
    if name not in packages:
        raise AptError(f"пакет не найден в репозитории: {name}")
    result = []
    for field in DEPENDENCY_FIELDS:
        for dep in parse_depends(packages[name].get(field, "")):
            if dep not in result:
                result.append(dep)
    return result