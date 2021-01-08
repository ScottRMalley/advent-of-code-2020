from shared import main


def preprocess(data_input):
    return [int(line) for line in data_input.strip().split('\n')]


def part1(data_input):
    values = preprocess(data_input)
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] + values[j] == 2020:
                return values[i]*values[j]


def part2(data_input):
    values = preprocess(data_input)
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            for k in range(j + 1, len(values)):
                if values[i] + values[j] + values[k] == 2020:
                    return values[i] * values[j] * values[k]


if __name__ == '__main__':
    main('input.txt', part1, part2)
