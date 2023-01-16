import re

def dict_to_obj(source: str) -> str:
    dico_references = re.findall(r"\[((?:\"|\'|\`)\w+(?:\"|\'|\`))\]", source)
    for reference in dico_references:
        s_quote = reference[0]
        e_quote = reference[-1]
        reference = reference[1:-1]
        source = source.replace('[' + s_quote + reference + e_quote + ']', '.' + reference)
    return source
