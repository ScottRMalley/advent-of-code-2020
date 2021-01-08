import copy

import numpy as np

from shared import main


def parse(i):
    if i == '.':
        return 0
    if i == '#':
        return 1
    if i == 'L':
        return -1


def filled_seats_part2(x, y, grid):
    num_filled = 0
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1)]
    for direction in directions:
        first = find_first_in_direction(direction, x, y, grid)
        if first > 0:
            num_filled += 1
    return num_filled


def filled_seats_part1(x, y, grid):
    dim_x, dim_y = grid.shape
    value = grid[x, y]
    around = grid[max(x - 1, 0): min(x + 2, dim_x), max(y - 1, 0): min(y + 2, dim_y)]
    selection = np.sum(np.sum(np.where(around > 0, 1, 0)))
    correction = 0
    if value > 0:
        correction += 1
    return selection - correction


def find_first_in_direction(direction, x, y, grid):
    dx, dy = direction
    dim_x, dim_y = grid.shape
    pos_x = x
    pos_y = y
    while True:
        if pos_x + dx >= dim_x or pos_x + dx < 0:
            break
        if pos_y + dy >= dim_y or pos_y + dy < 0:
            break
        if grid[pos_x + dx, pos_y + dy] != 0:
            return copy.deepcopy(grid[pos_x + dx, pos_y + dy])
        pos_x += dx
        pos_y += dy
    return 0


def update(grid, filled_seats_func, max_filled):
    dx, dy = grid.shape
    updated_grid = copy.deepcopy(grid)
    for x in range(dx):
        for y in range(dy):
            val = grid[x, y]
            if val == 0:
                continue
            num_filled = filled_seats_func(x, y, grid)
            if val == 1:
                if num_filled >= max_filled:
                    updated_grid[x, y] = -1
            if val == -1:
                if num_filled <= 0:
                    updated_grid[x, y] = 1
    return updated_grid


def update_till_end(grid, filled_seats_func=filled_seats_part1, max_filled=4):
    while True:
        updated_grid = update(grid, filled_seats_func, max_filled)
        if np.array_equal(grid, updated_grid):
            break
        grid = copy.deepcopy(updated_grid)
    return updated_grid


def preprocess(data_input):
    lines = data_input.strip().split('\n')
    a = []
    for line in lines:
        a.append([parse(x) for x in line])
    return np.array(a)


def part1(data_input):
    values = preprocess(data_input)
    final_grid = update_till_end(values)
    return np.sum(np.sum(np.where(final_grid > 0, 1, 0)))


def part2(data_input):
    values = preprocess(data_input)
    final_grid = update_till_end(values, filled_seats_func=filled_seats_part2, max_filled=5)
    return np.sum(np.sum(np.where(final_grid > 0, 1, 0)))


if __name__ == '__main__':
    main('input.txt', part1, part2)
