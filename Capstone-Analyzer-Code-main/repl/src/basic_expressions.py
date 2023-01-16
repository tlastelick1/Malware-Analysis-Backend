import re

def booleans(source: str) -> str:
    for expression in re.findall(r"(?:\s+)?(?:\!)?\!\[\]", source):
        operator = "true"
        if expression.count('!') == 1:
            operator = "false"
        spaces = expression.count(' ')
        if spaces == 0:
            spaces = 1
        source = source.replace(expression, (spaces * ' ') + operator)
    return source


def operators(source: str) -> str:
    for operation in re.findall(r"[-\+]+", source):
        # incrementation / decrementation
        if operation == "--" or operation == "++":
            continue
        minus = (operation.count("-")) % 2 == 1
        source = source.replace(operation, "-" if minus else "+")
    source = source.replace("- -", '+')
    return source


def integers(source: str) -> str:
    for hexa_number in re.findall(r"0x[a-f0-9]+", source):
        deci_number = int(hexa_number, 16)
        source = source.replace(hexa_number, str(deci_number), 1)
    return source
