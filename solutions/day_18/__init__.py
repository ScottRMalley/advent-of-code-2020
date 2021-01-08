from shared import main
import re
import copy


def preprocess(data_input):
    return [s.strip() for s in data_input.strip().split('\n')]


def calculate(eq_no_parentheses):
    eq = eq_no_parentheses.split(' ')
    current_val = int(eq[0])
    i = 1
    while i < len(eq) - 1:
        if eq[i] == '*':
            current_val *= int(eq[i + 1])
        if eq[i] == '+':
            current_val += int(eq[i + 1])
        i += 2
    return current_val


def calculate_plus_first(eq_no_parentheses):
    eq_no_plus = handle_all_plus(eq_no_parentheses)
    equation = eq_no_plus.split(' ')
    current_val = int(equation[0])
    i = 1
    while i < len(equation) - 1:
        if equation[i] == '*':
            current_val *= int(equation[i + 1])
        i += 2
    return current_val


def parse_equation(eq):
    while eq.find('(') != -1:
        innermost = re.findall(r'\(([^\(^\)]+)\)', eq)
        for exp in innermost:
            eq = eq.replace('(' + exp + ')', str(calculate(exp)))
    return calculate(eq)


def parse_equation_plus_first(eq):
    while eq.find('(') != -1:
        innermost = re.findall(r'\(([^\(^\)]+)\)', eq)
        for exp in innermost:
            eq = eq.replace('(' + exp + ')', str(calculate_plus_first(exp)))
    return calculate_plus_first(eq)


def handle_all_plus(eq):
    while eq.find('+') != -1:
        additions = re.findall(r'\d+\s\+\s\d+', eq)
        for add in additions:
            vals = add.split(' ')
            sum_val = str(int(vals[0]) + int(vals[-1]))
            eq = replace_operation(add, eq, sum_val)
    return eq


def replace_operation(op, eq, val):
    return re.sub(r'\b{}\b'.format(op.replace(' ', r'\s').replace('+', r'\+')), val, eq)


def part1(data_input):
    values = preprocess(data_input)
    total = 0
    for eq in values:
        total += parse_equation(eq)
    return total


def part2(data_input):
    v = preprocess(data_input)
    t = 0
    for e in v:
        t += parse_equation_plus_first(e)
    return t


if __name__ == '__main__':
    main('input.txt', part1, part2)
