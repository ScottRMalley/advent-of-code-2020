from shared import main


def preprocess(data_input):
    return [int(i) for i in data_input.strip()]


def pick_up(current_ind, cups):
    picked = []
    for i in range(current_ind+1, current_ind + 4):
        picked.append(cups[i % len(cups)])
        del cups[i % len(cups)]
    return picked


def play_round(current, cups):
    current_ind = cups.index(current)
    print(f'Current cup')
    picked_up = pick_up(current_ind, cups)


def part1(data_input):
    values = preprocess(data_input)
    print(values)
    return None


def part2(data_input):
    values = preprocess(data_input)
    return None


if __name__ == '__main__':
    main('test-input.txt', part1, part2)
