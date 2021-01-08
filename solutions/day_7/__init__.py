import re

from shared import main


def parse_bag_line(line):
    colors = re.findall(r'[a-z]+\s[a-z]+(?=\sbag)', line)
    numbers = re.findall(r'([0-9])', line)
    containing_bags = {}
    for index, color in enumerate(colors[1:]):
        if color != 'no other':
            containing_bags[color] = int(numbers[index])
    return colors[0], containing_bags


def can_hold(color, contained_bag_color, rules):
    containing_bags = rules[color]
    if len(containing_bags.keys()) < 1:
        return False
    if contained_bag_color in containing_bags.keys():
        return True
    return any([can_hold(bag_color, contained_bag_color, rules) for bag_color in containing_bags.keys()])


def count_bags_inside(color, rules):
    containing_bags = rules[color]
    if len(containing_bags.keys()) == 0:
        return 0
    count = 0
    for bag_color in containing_bags.keys():
        count += containing_bags[bag_color] * (1 + count_bags_inside(bag_color, rules))
    return count


def preprocess(data_input):
    rules = {}
    for row in data_input.strip().split('\n'):
        color, containing_bags = parse_bag_line(row)
        rules[color] = containing_bags
    return rules


def part1(data_input):
    rules = preprocess(data_input)
    with_gold_bag = []
    for color in rules.keys():
        if can_hold(color, 'shiny gold', rules):
            with_gold_bag.append(color)
    return len(with_gold_bag)


def part2(data_input):
    rules = preprocess(data_input)
    return count_bags_inside('shiny gold', rules)


if __name__ == '__main__':
    main('input.txt', part1, part2)
