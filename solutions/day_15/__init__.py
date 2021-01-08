from shared import main


def memory_game(numbers, end_turn):
    last_spoken = numbers[-1]
    spoken_numbers = {numbers[i]: i + 1 for i in range(len(numbers))}
    start_turn = len(numbers) + 1

    for turn in range(start_turn, end_turn + 1):
        if last_spoken not in spoken_numbers:
            spoken_numbers[last_spoken] = turn - 1
            last_spoken = 0
        else:
            last_turn_spoken = spoken_numbers[last_spoken]
            spoken_numbers[last_spoken] = turn - 1
            last_spoken = (turn - 1) - last_turn_spoken

    return last_spoken


def preprocess(data_input):
    return [int(k) for k in data_input.strip().split(',')]


def part1(data_input):
    values = preprocess(data_input)
    return memory_game(values, 2020)


def part2(data_input):
    values = preprocess(data_input)
    return memory_game(values, 30000000)


if __name__ == '__main__':
    main('input.txt', part1, part2)
