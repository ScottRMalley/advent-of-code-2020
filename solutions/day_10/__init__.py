from shared import main
import numpy as np


def find_nexts(adapter_index, adapters):
    potential_adapters = adapters[adapter_index + 1:]
    nexts = []
    for k, adapter in enumerate(potential_adapters):
        if 0 < adapter - adapters[adapter_index] <= 3:
            nexts.append(k + adapter_index + 1)
        else:
            break
    return nexts


all_chains_cache = {}


def find_all_chains(adapter_index, adapters):
    if adapter_index in all_chains_cache:
        return all_chains_cache[adapter_index]
    else:
        if adapter_index == len(adapters) - 1:
            return 1
        nexts = find_nexts(adapter_index, adapters)
        all_chains = sum([find_all_chains(n, adapters) for n in nexts])
        all_chains_cache[adapter_index] = all_chains
        return all_chains


def find_all_chains_nonrecursive(adapters):
    paths_per_jolt = [0 for i in range(max(adapters) + 1)]
    paths_per_jolt[0] = 1
    for adapter in adapters[1:]:
        paths_per_jolt[adapter] = sum(paths_per_jolt[max(adapter - 3, 0):adapter])
    return paths_per_jolt[adapters[-1]]


def preprocess(data_input):
    ad = [int(i) for i in data_input.strip().split('\n')]
    ad.append(0)
    ad.append(max(ad) + 3)
    return np.array(ad)


def part1(data_input):
    values = preprocess(data_input)
    sorted_adapters = np.sort(values)
    diff = sorted_adapters[1:] - sorted_adapters[:-1]
    return np.sum(np.where(diff == 1, 1, 0)) * np.sum(np.where(diff == 3, 1, 0))


def part2(data_input):
    values = preprocess(data_input)
    values = np.sort(values)
    #return find_all_chains(0, values)
    return find_all_chains_nonrecursive(values)


if __name__ == '__main__':
    main('input.txt', part1, part2)
