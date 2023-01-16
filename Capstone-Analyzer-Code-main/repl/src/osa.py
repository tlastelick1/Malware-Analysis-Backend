"""
OSA : Obfuscated strings array

The OSA refers to an array at the top of an obfuscated JavaScript file. In this array
there are encoded strings (it can also be unicode-encoded). Then, this array is used
in the obfuscated code to refer at this string, which JavaScript is able to decode
and then use in it's runtime.

These string are important since then can contain a module's name to importe, an
error code, a specific API URL the creator tries to hide, and so on ... Although more
often it's some console.log stuff such as credit or else.

Anyway, this array is sometime let as it is, but in some case, this array is
shuffled before it's used, and after it's declared. This process makes the
deobfuscation harder. For now, it's not handled. It might be in the future.
"""

import re

# --- FONCTIONS ---


def get_source(path: str) -> str:
    source = ""
    with open(path, "r") as s:
        source = s.read()
    return source


def find_osa_name(source: str) -> str:
    match = re.search(r"^var (_[a-f0-9]+x[a-f0-9]+(?:x[a-f0-9]+)?)=", source)
    return match[1] if match is not None else None


def get_osa_content(source: str) -> str:
    array = []
    is_string = False
    string = ""
    quotes = ("\"", "'", "`")
    quote_mark = None

    for c in source:
        if c == ']' and not is_string:
            break

        if c in quotes and quote_mark is None:
            quote_mark = c

        if not is_string and c == quote_mark:
            is_string = True
            continue

        if is_string and c == quote_mark:
            is_string = False
            array.append(string)
            string = ""
            quote_mark = None
            continue

        if is_string and c != quote_mark:
            string += c
            continue

    return array


def use_osa_content(source: str, osa_name: str, osa_content: list) -> str:
    done = 0
    for i, e in enumerate(osa_content):
        try:
            source.index(osa_name + '[' + str(i) + ']')
        except:
            continue
        else:
            source = source.replace(
                osa_name + '[' + str(i) + ']',
                '"' + e.encode().decode("unicode-escape") + '"'
            )
            done += 1
    if done < len(osa_content):
        return source
    slice_range = 0
    slice_range += len("var " + osa_name + "=[")
    slice_range += sum([len(e) + 2 for e in osa_content])
    slice_range += len(osa_content) - 1
    slice_range += len("];")
    source = source[slice_range:]
    return source

# --- TESTS ---


def test_find_osa_name():
    source = get_source("../examples/choco8exe/index.js")
    assert find_osa_name(source) == "_0xb892"
    source = get_source("../examples/social-404/index.js")
    assert find_osa_name(source) == "_0x9a10"


def test_get_osa_content():
    source = get_source("../examples/choco8exe/index.js")
    array = get_osa_content(source)
    assert len(array) > 0, "Arrays are rarely empty ..."
    source = get_source("../examples/social-404/index.js")
    array = get_osa_content(source)
    assert len(array) > 0, "Arrays are rarely empty ..."


def test():
    source = get_source("../examples/choco8exe/index.js")
    osa_name = find_osa_name(source)
    assert osa_name is not None
    osa_content = get_osa_content(source)
    source = use_osa_content(source, osa_name, osa_content)
    return source


if __name__ == "__main__":
    test_find_osa_name()
    test_get_osa_content()
