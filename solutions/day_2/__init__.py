from shared import main


def preprocess(data_input):
    values = []
    for line in data_input.strip().split('\n'):
        args = line.split(' ');
        between = args[0].split('-')
        n_min = int(between[0])
        n_max = int(between[1])
        character = args[1].strip(':')
        password = args[2]
        values.append((character, n_min, n_max, password))
    return values


def validate_password_part1(character, n_min, n_max, password):
    return n_min <= password.count(character) <= n_max


def validate_password_part2(character, n_min, n_max, password):
    first_loc = password[n_min - 1]
    second_loc = password[n_max - 1]
    return '{}{}'.format(first_loc, second_loc).count(character) == 1


def part1(data_input):
    values = preprocess(data_input)
    num_valid = 0
    for character, n_min, n_max, password in values:
        if validate_password_part1(character, n_min, n_max, password):
            num_valid += 1
    return num_valid


def part2(data_input):
    values = preprocess(data_input)
    num_valid = 0
    for character, n_min, n_max, password in values:
        if validate_password_part2(character, n_min, n_max, password):
            num_valid += 1
    return num_valid


if __name__ == '__main__':
    main('input.txt', part1, part2)
