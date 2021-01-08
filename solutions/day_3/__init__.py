import numpy as np
import pandas as pd

from shared import main


def preprocess(data_input):
    values = []
    for line in data_input.strip().split('\n'):
        values.append([0 if i == '.' else 1 for i in line])
    return np.array(values)


def check_slope(grid, dx, dy):
    Ny, Nx = grid.shape
    ys = np.arange(0, Ny, dy)
    xs = dx * np.arange(0, len(ys)) % Nx
    return np.sum(grid[ys, xs])


def part1(data_input):
    grid = preprocess(data_input)
    return check_slope(grid, 3, 1)


def part2(data_input):
    grid = preprocess(data_input)
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    ntrees = np.array([check_slope(grid, *slope) for slope in slopes])
    return np.prod(ntrees)


if __name__ == '__main__':
    main('input.txt', part1, part2)
