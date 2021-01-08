from shared import main
import numpy as np


def preprocess(data_input):
    return [int(val) for val in data_input.strip().split('\n')]


def check_addition(array, val):
    for i in array:
        for j in array:
            if i + j == val:
                return True
    return False


def find_contiguous_sum(v, vs):
    vs = np.array(vs)
    n = len(vs)
    for k in range(n):
        start = k
        for j in range(k + 1, n):
            end = j
            vs_slice = vs[start:end]
            total = np.sum(vs_slice)
            if total == v:
                return np.min(vs_slice) + np.max(vs_slice)
    return None


def part1(data_input):
    values = preprocess(data_input)
    for k in range(25, len(values)):
        previous_25 = values[k - 25:k]
        if not check_addition(previous_25, values[k]):
            return values[k]
    return None


def part2(data_input):
    values = preprocess(data_input)
    value = part1(data_input)
    r = find_contiguous_sum(value, values)
    return None


if __name__ == '__main__':
    main('input.txt', part1, part2)
