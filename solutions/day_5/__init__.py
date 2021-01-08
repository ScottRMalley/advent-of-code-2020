import math

from shared import main


def find_position(rs, first, last):
    if len(rs) == 1:
        if rs[0] == 'F' or rs[0] == 'L':
            return first
        return last
    if rs[0] == 'F' or rs[0] == 'L':
        return find_position(rs[1:], first, first + (last - first) // 2)
    return find_position(rs[1:], first + math.ceil((last - first) / 2), last)


def find_seat_id(id_string):
    rs = id_string[0:7]
    row = find_position(rs, 0, 127)
    rc = id_string[7:10]
    column = find_position(rc, 0, 7)
    seat_id = row * 8 + column
    return seat_id


def preprocess(data_input):
    return data_input.strip().split('\n')


def part1(data_input):
    values = preprocess(data_input)
    return max([find_seat_id(item) for item in values])


def part2(data_input):
    values = preprocess(data_input)
    seat_ids = sorted([find_seat_id(item) for item in values])
    for i in range(len(seat_ids) - 1):
        if seat_ids[i + 1] != seat_ids[i] + 1:
            return seat_ids[i] + 1
    return -1


if __name__ == '__main__':
    main('input.txt', part1, part2)
