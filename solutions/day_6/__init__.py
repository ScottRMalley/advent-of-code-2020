from collections import defaultdict

import numpy as np

from shared import main


def parse_input_line(line):
    return line


def split(word):
    return [char for char in word]


def preprocess(data_input):
    groups = data_input.strip().split('\n\n')
    dict_objects = []
    for group in groups:
        dict_obj = defaultdict(int)
        for member in group.strip().split('\n'):
            dict_obj['total_members'] += 1
            for answer in member:
                dict_obj[answer] += 1
        dict_objects.append(dict_obj)
    return dict_objects


def part1(data_input):
    group_answers = preprocess(data_input)
    return np.sum(np.array([len(answers.keys()) - 1 for answers in group_answers]))


def part2(data_input):
    group_answers = preprocess(data_input)
    all_yes = 0
    for answers in group_answers:
        for answer in answers:
            if answer != 'total_members' and answers[answer] == answers['total_members']:
                all_yes += 1
    return all_yes


if __name__ == '__main__':
    main('input.txt', part1, part2)
