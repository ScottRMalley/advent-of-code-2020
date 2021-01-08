import re


def validate_passport_keys(passport):
    req_keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    for req_key in req_keys:
        if req_key not in passport:
            return False
    return True


def valid_byr(byr):
    if len(byr) != 4:
        return False
    return 1920 <= int(byr) <= 2002


def valid_iyr(iyr):
    if len(iyr) != 4:
        return False
    return 2010 <= int(iyr) <= 2020


def valid_eyr(eyr):
    if len(eyr) != 4:
        return False
    return 2020 <= int(eyr) <= 2030


def valid_hgt(hgt):
    if not hgt[:-2].isnumeric():
        return False
    if hgt[-2:] == 'cm':
        return 150 <= int(hgt[:-2]) <= 193
    if hgt[-2:] == 'in':
        return 59 <= int(hgt[:-2]) <= 76
    return False


def valid_hcl(hcl):
    if hcl[0] != '#':
        return False
    return re.match('([0-9]|[a-f]){6}', hcl[1:]) is not None


def valid_ecl(ecl):
    allowed = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    return ecl in allowed


def valid_pid(pid):
    if len(pid) != 9:
        return False
    return pid.isnumeric()


def validate_key_value(key, value):
    switcher = {
        'byr': valid_byr,
        'iyr': valid_iyr,
        'eyr': valid_eyr,
        'hgt': valid_hgt,
        'hcl': valid_hcl,
        'ecl': valid_ecl,
        'pid': valid_pid,
        'cid': lambda arg: True
    }
    return switcher[key](value)


def validate_passport(passport):
    if not validate_passport_keys(passport):
        return False
    for key, value in passport.items():
        if not validate_key_value(key, value):
            return False
    return True


def part1(data_input):
    passports = preprocess(data_input)
    valid = 0
    for passport in passports:
        if validate_passport_keys(passport):
            valid += 1
    return valid


def part2(data_input):
    passports = preprocess(data_input)
    valid = 0
    for passport in passports:
        if validate_passport(passport):
            valid += 1
    return valid


def preprocess(data_input):
    data_objects = []
    for line in data_input.split('\n\n'):
        dict_obj = {}
        for item in line.replace('\n', ' ').strip().split(' '):
            data = item.split(':')
            dict_obj[data[0]] = data[1]
        data_objects.append(dict_obj)
    return data_objects


if __name__ == "__main__":
    main('input.txt', part1, part2)
