from shared import main
import regex as re


def preprocess(data_input):
    rule_lines, data = data_input.strip().split('\n\n')
    rules = {}
    for r in rule_lines.strip().split('\n'):
        n, r_string = r.split(': ')
        rules[n] = r_string.replace('"', '')
    data = data.strip().split('\n')
    return rules, data


def replace_rule_placeholder(rule, rules, current_regex):
    if rules[rule] == 'a' or rules[rule] == 'b':
        return current_regex.replace(f'[{rule}]', rules[rule])
    if rules[rule].find('|') != -1:
        replace_string = parse_or_rule(rules[rule])
        return current_regex.replace(f'[{rule}]', replace_string)
    replace_rules = rules[rule].split(' ')
    replace_string = ''
    for r in replace_rules:
        replace_string += f'[{r}]'
    return current_regex.replace(f'[{rule}]', '(' + replace_string + ')')


def parse_or_rule(rule_string):
    before, after = rule_string.split('|')
    before_group = ''
    after_group = ''
    for num in before.strip().split(' '):
        before_group += f'[{num}]'
    for num in after.strip().split(' '):
        after_group += f'[{num}]'
    return f'({before_group}|{after_group})'


def get_regex(start_rule, rules):
    current_regex = f'[{start_rule}]'
    while current_regex.find('[') != -1:
        remaining_rules = re.findall(r'\[(\d+)\]', current_regex)
        for r in remaining_rules:
            current_regex = replace_rule_placeholder(r, rules, current_regex)
    return current_regex


def matches_regex_exact(data_line, regex):
    m = regex.match(data_line)
    matches = False
    if m is not None:
        if m.group() == data_line:
            matches = True
    return matches


def part1(data_input):
    rules, data = preprocess(data_input)
    regex_string = get_regex('0', rules)
    regex = re.compile(regex_string)
    num_matches = 0
    for d in data:
        if matches_regex_exact(d, regex):
            num_matches += 1
    return num_matches


def part2(data_input):
    rules, data = preprocess(data_input)
    rules['8'] = '42 | 42 8'
    rules['11'] = '42 31 | 42 11 31'
    regex_42 = get_regex('42', rules)
    regex_31 = get_regex('31', rules)
    regex_8 = f'(({regex_42})+?)'
    regex_11 = lambda n: f'(?P<eleven{n}>{regex_42}(?:|(?&eleven{n})){regex_31})'
    regex_string = get_regex_loops('0', rules, regex_8, regex_11)
    regex = re.compile(regex_string)

    num_matches = 0
    for i, d in enumerate(data):
        if matches_regex_exact(d, regex):
            num_matches += 1
    return num_matches


def get_regex_loops(start_rule, rules, regex_8, regex_11):
    current_regex = f'[{start_rule}]'
    n11 = 0
    while current_regex.find('[') != -1:
        current_regex = current_regex.replace('[8]', regex_8)
        while current_regex.find('[11]') != -1:
            current_regex = current_regex.replace('[11]', regex_11(n11), 1)
            n11 += 1
        remaining_rules = re.findall(r'\[(\d+)\]', current_regex)
        for r in remaining_rules:
            current_regex = replace_rule_placeholder(r, rules, current_regex)
    return current_regex


if __name__ == '__main__':
    main('input.txt', part1, part2)
