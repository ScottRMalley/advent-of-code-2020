import numpy as np

from shared import main


def preprocess(data_input):
    lines = data_input.strip().split('\n');
    grid = np.zeros((len(lines[0]), len(lines), 1))
    for i, line in enumerate(lines):
        row = [1 if c == '#' else 0 for c in line.strip()]
        for j, val in enumerate(row):
            if val == 1:
                grid[i, j, 0] = 1
    return grid


def cycle(previous_state):
    dx, dy, dz = previous_state.shape
    new_state = np.zeros((dx + 2, dy + 2, dz + 2))
    previous_state = np.pad(previous_state, ((1, 1), (1, 1), (1, 1)), 'constant',
                            constant_values=((0, 0), (0, 0), (0, 0)))
    ndx, ndy, ndz = new_state.shape
    for x in range(ndx):
        for y in range(ndy):
            for z in range(ndz):
                neighbor_slice = previous_state[max(x - 1, 0): min(x + 2, ndx), max(y - 1, 0): min(y + 2, ndy),
                                 max(z - 1, 0): min(z + 2, ndz)]
                num_active = np.sum(np.sum(np.sum(neighbor_slice)))
                if previous_state[x, y, z] == 1:
                    if num_active == 3 or num_active == 4:
                        new_state[x, y, z] = 1
                else:
                    if num_active == 3:
                        new_state[x, y, z] = 1
    return new_state


def cycle_4d(previous_state):
    dx, dy, dz, dw = previous_state.shape
    new_state = np.zeros((dx + 2, dy + 2, dz + 2, dw + 2))
    previous_state = np.pad(previous_state, ((1, 1), (1, 1), (1, 1), (1, 1)), 'constant',
                            constant_values=((0, 0), (0, 0), (0, 0), (0, 0)))
    ndx, ndy, ndz, ndw = new_state.shape
    for x in range(ndx):
        for y in range(ndy):
            for z in range(ndz):
                for w in range(ndw):
                    neighbor_slice = previous_state[max(x - 1, 0): min(x + 2, ndx), max(y - 1, 0): min(y + 2, ndy),
                                     max(z - 1, 0): min(z + 2, ndz), max(w - 1, 0): min(w + 2, ndw)]
                    num_active = np.sum(np.sum(np.sum(np.sum(neighbor_slice))))
                    if previous_state[x, y, z, w] == 1:
                        if num_active == 3 or num_active == 4:
                            new_state[x, y, z, w] = 1
                    else:
                        if num_active == 3:
                            new_state[x, y, z, w] = 1
    return new_state


def part1(data_input):
    initial_state = preprocess(data_input)
    new_state = cycle(initial_state)
    for i in range(5):
        new_state = cycle(new_state)
    total_active = np.sum(np.sum(np.sum(new_state)))
    return total_active


def part2(data_input):
    initial_state = preprocess(data_input)
    dx, dy, dz = initial_state.shape
    initial_state = initial_state.reshape((dx, dy, dz, 1))
    new_state = cycle_4d(initial_state)
    for i in range(5):
        new_state = cycle_4d(new_state)
    total_active = np.sum(np.sum(np.sum(np.sum(new_state))))
    return total_active


if __name__ == '__main__':
    main('input.txt', part1, part2)
