import re


def escape_string(source: str) -> str:
    escaped_strings = re.findall(
        r"(?:\"|\'|\`)(?:(?:\\(?:u|x)[0-9A-F]+)+)(?:\"|\'|\`)", source)
    for string in escaped_strings:
        s_quote = string[0]
        e_quote = string[-1]
        decoded = string[1:-1].encode().decode("unicode-escape")
        source = source.replace(
            string, s_quote + decoded + e_quote)
    return source
