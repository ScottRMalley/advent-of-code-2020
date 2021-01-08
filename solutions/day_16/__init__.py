from collections import defaultdict

from shared import main
import re


def get_field(val):
    digits = [(int(v.split('-')[0]), int(v.split('-')[1])) for v in re.findall(r'[0-9]+-[0-9]+', val)]
    return digits


def preprocess(data_input):
    lines = data_input.strip().split('\n\n')
    fields = [get_field(val) for val in lines[0].strip().split('\n')]
    yours = [int(n) for n in lines[1].strip().split('\n')[1].split(',')]
    others = []
    for l in lines[2].strip().split('\n')[1:]:
        others.append([int(j) for j in l.strip().split(',')])
    return fields, yours, others


def check_totally_invalid(rules, ticket_value):
    for rule in rules:
        if rule[0][0] <= ticket_value <= rule[0][1] or rule[1][0] <= ticket_value <= rule[1][1]:
            return False
    return True


def check_rule(rule, ticket_value):
    return rule[0][0] <= ticket_value <= rule[0][1] or rule[1][0] <= ticket_value <= rule[1][1]


def remove_totally_invalid(rules, tickets):
    valid_tickets = []
    for ticket in tickets:
        valid_ticket = True
        for val in ticket:
            if check_totally_invalid(rules, val):
                valid_ticket = False
        if valid_ticket:
            valid_tickets.append(ticket)
    return valid_tickets


def get_rule_mapping(rules, valid_tickets):
    mapping_dict = defaultdict(list)
    for j in range(len(rules)):
        for k in range(len(valid_tickets[0])):
            works = True
            for ticket in valid_tickets:
                if not check_rule(rules[j], ticket[k]):
                    works = False
            if works:
                mapping_dict[j].append(k)

    result = {}
    while len(result) < len(rules):
        for key in mapping_dict:
            if len(mapping_dict[key]) == 1:
                result[key] = mapping_dict[key][0]
        remove_known(mapping_dict, result)
    return result


def remove_known(current_mapping, known):
    for fk in known:
        for key in current_mapping:
            if known[fk] in current_mapping[key]:
                current_mapping[key].remove(known[fk])
        if fk in current_mapping:
            del current_mapping[fk]
    return current_mapping


def validate_mapping(rules, valid_tickets, mapping):
    for ticket in valid_tickets:
        for i in range(len(ticket)):
            if not check_rule(rules[i], ticket[mapping[i]]):
                print(ticket[mapping[i]], rules[i])
                print(i, mapping[i])
                print('Invalid mapping!')


def part1(data_input):
    fields, yours, others = preprocess(data_input)
    total = 0
    for t in others:
        for val in t:
            if check_totally_invalid(fields, val):
                total += val
    return total


def part2(data_input):
    fields, yours, others = preprocess(data_input)
    valid_tickets = remove_totally_invalid(fields, others)
    mapping = get_rule_mapping(fields, valid_tickets)
    validate_mapping(fields, valid_tickets, mapping)
    result = 1
    for m in mapping:
        if m < 6:
            result *= yours[mapping[m]]
    return result


if __name__ == '__main__':
    main('input.txt', part1, part2)
