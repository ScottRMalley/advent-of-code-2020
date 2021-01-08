from shared import main
import numpy as np
import matplotlib.pyplot as plt


def follow_by_instruction(pos, v, instruction):
    if np.isscalar(instruction):
        return pos + instruction * v, v
    dim = len(instruction.shape)
    if dim == 1:
        return pos + instruction, v
    return pos, np.dot(instruction, v)


def follow_by_waypoint(pos, waypoint, instruction):
    if np.isscalar(instruction):
        return pos + instruction * waypoint, waypoint
    dim = len(instruction.shape)
    if dim == 1:
        return pos, waypoint + instruction
    return pos, np.dot(instruction, waypoint)


def follow_all_by_instructions(pos, waypoint, instructions):
    xs = [pos[0]]
    ys = [pos[1]]
    for instruction in instructions:
        pos, waypoint = follow_by_instruction(pos, waypoint, instruction)
        xs.append(pos[0])
        ys.append(pos[1])
    return np.array(xs), np.array(ys)


def follow_all_by_waypoint(pos, v, instructions):
    xs = [pos[0]]
    ys = [pos[1]]
    for instruction in instructions:
        pos, v = follow_by_waypoint(pos, v, instruction)
        xs.append(pos[0])
        ys.append(pos[1])
    return np.array(xs), np.array(ys)


def R(degrees):
    theta = np.radians(degrees)
    c, s = np.cos(theta), np.sin(theta)
    return np.array(((c, -s), (s, c)))


def preprocess(data_input):
    lines = data_input.strip().split('\n')
    directions = {'N': np.array([0, 1]),
                  'E': np.array([1, 0]),
                  'S': np.array([0, -1]),
                  'W': np.array([-1, 0])
                  }
    rotations = {
        'F': 1,
        'R': np.array([[1, -1], [-1, 1]]),
        'L': np.array([[1, 1], [1, 1]])
    }

    instructions = []

    for line in lines:
        d = line[0]
        v = int(line[1:])
        if d in directions:
            instructions.append(directions[d] * v)
        elif d in rotations:
            if d == 'F':
                instructions.append(v)
            else:
                instructions.append(rotations[d] * R(v))
    return instructions


def part1(data_input):
    values = preprocess(data_input)
    pos = np.array([0, 0])
    v = np.array([1, 0])
    xs, ys = follow_all_by_instructions(pos, v, values)
    return int(np.round(np.absolute(xs[-1] - xs[0]) + np.absolute(ys[-1] - ys[0])))


def part2(data_input):
    values = preprocess(data_input)
    pos = np.array([0, 0])
    v = np.array([10, 1])
    xs, ys = follow_all_by_waypoint(pos, v, values)
    plt.plot(xs, ys)
    plt.show()
    return int(np.round(np.absolute(xs[-1] - xs[0]) + np.absolute(ys[-1] - ys[0])))


if __name__ == '__main__':
    main('input.txt', part1, part2)
