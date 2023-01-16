import re

def replace_names(source: str) -> str:
    i = 0
    for name in re.findall(r"(_[a-f0-9]+x[a-f0-9]+(?:x[a-f0-9]+)?)", source):
        new_name = "LOCAL_" + str(i) + '_'
        i += 1
        source = source.replace(name, new_name)
    return source

def unused_names(source: str) -> str:
    i = 0
    for name in re.findall(r"(_[a-f0-9]+x[a-f0-9]+(?:x[a-f0-9]+)?)", source):
        usage = source.count(name)
        if usage <= 1:
            new_name = "UNUSED_" + str(i) + '_'
            i += 1
            source = source.replace(name, new_name)
    return source

def capture_unused_function(source: str, match: str) -> str:
    index = source.find(match)
    i = index + len(match)
    while True:
        char = source[i]
        match += char
        if char == '{':
            break
        i += 1
    levels = 1
    counter = 0
    while levels > 0:
        counter += 1
        char = source[i + counter]
        match += char
        if char == '}':
            levels -= 1
        if char == '{':
            levels += 1
    return match

def remove_unused_function(source: str) -> str:
    for detector in (
        r"UNUSED_\d+_=function\(",
        r"function UNUSED_\d+_\("
    ):
        for match in re.findall(detector, source):
            match = capture_unused_function(source, match)
            rep = ''
            if source[source.index(match) + len(match)] == ',':
                match += ','
            if source[source.index(match) - 1] == ',':
                match = ',' + match
                rep = ';'
            source = source.replace(match, rep, 1)
    return source
