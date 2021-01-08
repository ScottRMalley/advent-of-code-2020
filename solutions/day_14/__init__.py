from shared import main
import re
import numpy as np


def preprocess(data_input):
    lines = data_input.strip().split('\n')
    instructions = []
    for line in lines:
        vals = line.split(' = ')
        if vals[0][0:4] == 'mask':
            instructions.append({'op': 'mask', 'val': vals[1]})
        elif vals[0][0:3] == 'mem':
            instructions.append({'op': 'mem', 'val': int(vals[1]), 'ind': int(re.findall(r'\d+', vals[0])[0])})
    return instructions


def run_program(instructions):
    mem_size = max([instruction['ind'] for instruction in instructions if instruction['op'] == 'mem']) + 1
    memory = np.zeros(mem_size, dtype=int)
    bit_mask = convert_to_bits(0)

    for instruction in instructions:
        if instruction['op'] == 'mask':
            bit_mask = instruction['val']
        elif instruction['op'] == 'mem':
            n_int = instruction['val']
            n_ind = instruction['ind']
            masked = apply_mask(bit_mask, n_int)
            memory[n_ind] = masked
    return np.sum(memory)


def convert_to_bits(n_int):
    return '{0:036b}'.format(n_int)


def convert_to_int(bit_string):
    return int(bit_string, 2)


def apply_mask(bit_mask, n_int):
    n_bits_array = [c for c in convert_to_bits(n_int)]
    for i, bit in enumerate(bit_mask):
        if bit != 'X':
            n_bits_array[i] = bit
    bit_string = ''
    for c in n_bits_array:
        bit_string += c
    return convert_to_int(bit_string)


def run_program_part_2(instructions):
    mem_size = max([instruction['ind'] for instruction in instructions if instruction['op'] == 'mem']) + 1
    memory = {}
    bit_mask = convert_to_bits(0)

    for instruction in instructions:
        if instruction['op'] == 'mask':
            bit_mask = instruction['val']
        elif instruction['op'] == 'mem':
            n_int = instruction['val']
            n_ind = instruction['ind']
            addresses = get_addresses(bit_mask, n_ind)
            for a in addresses:
                memory[a] = n_int
    return sum(memory.values())


def get_addresses(mask, n_ind):
    cache = []
    masked = apply_mask_address(mask, convert_to_bits(n_ind))
    permute_address(0, masked, cache)
    return [convert_to_int(bs) for bs in cache]


def permute_address(n, address, cache):
    if n > len(address) - 1:
        cache.append(address)
        return
    if address[n] == 'X':
        permute_address(n + 1, address[:n] + '0' + address[n + 1:], cache)
        permute_address(n + 1, address[:n] + '1' + address[n + 1:], cache)
    else:
        permute_address(n + 1, address, cache)


def apply_mask_address(mask, address):
    mask_array = [c for c in mask]
    address_array = [c for c in address]
    for i, m_val in enumerate(mask_array):
        if m_val == 'X' or m_val == '1':
            address_array[i] = m_val
    return to_string(address_array)


def to_string(array):
    result = ''
    for a in array:
        result += a
    return result


def part1(data_input):
    values = preprocess(data_input)
    return run_program(values)


def part2(data_input):
    values = preprocess(data_input)
    return run_program_part_2(values)


if __name__ == '__main__':
    main('input.txt', part1, part2)
