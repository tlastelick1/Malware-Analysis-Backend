import re


def isolate_weird_cases(number: str) -> str:
    if number[0] == '0' and len(number) > 1:
        while number[0] == '0':
            number = number[1:]
    return number


def evaluator(result: float, number: float, op: str) -> float:
    if op == '-':
        result -= number
    elif op == '+':
        result += number
    elif op == '*':
        result *= number
    elif op == '/':
        result /= number
    elif op == '%':
        result %= number
    return result


def do_the_maths(source: str) -> str:
    for math in re.findall(r"(?:[-\+\/\*%]\d+(?:\.\d+)?)+", source):
        numbers = re.findall(r"\d+", math)
        operators = re.findall(r"[\-\+\*\/%]", math)
        result = float(numbers[0])
        i = 0
        for number in numbers:
            op = operators[i]
            number = isolate_weird_cases(number)
            result = evaluator(result, float(number), op)
            i += 1
        if '.' in str(result) and int(str(result).split('.')[-1]) == 0:
            result = int(str(result).split('.')[0])
        source = source.replace(math, str(result), 1)
    return source
