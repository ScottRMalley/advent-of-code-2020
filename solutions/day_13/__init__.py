import numpy as np

from shared import main


def get_earliest_departure(time, buses):
    max_k = int(np.ceil(float(time) / np.min(buses[buses > 0])))
    schedule = np.tile(buses, (max_k - 1, 1)).T * np.arange(1, max_k)
    bus_locs, y_locs = np.where(schedule >= time)
    depart = np.argmin(schedule[bus_locs, y_locs])
    depart_time = schedule[bus_locs, y_locs][depart]
    depart_bus = buses[bus_locs[depart]]
    return depart_bus, depart_time


def check_bus_staggered_start(start_time, buses, offset):
    for i in range(len(buses)):
        if not ((start_time + offset[i]) % buses[i] == 0):
            return False
    return True


def find_staggered_depart_time(buses):
    valid_bus_index = np.where(buses > 0)[0]
    valid_buses = buses[valid_bus_index]
    max_bus_ind = np.argmax(buses)
    start_time = buses[max_bus_ind] - max_bus_ind
    while True:
        if check_bus_staggered_start(start_time, valid_buses, valid_bus_index):
            return start_time
        start_time += buses[max_bus_ind]


def preprocess(data_input):
    lines = data_input.strip().split('\n')
    t = int(lines[0])
    buses = np.array([int(c) if c != 'x' else -1 for c in lines[1].strip().split(',')], dtype=int)
    return t, buses


def part1(data_input):
    t, values = preprocess(data_input)
    bus, time = get_earliest_departure(t, values)
    return bus * (time - t)


def part2(data_input):
    _, values = preprocess(data_input)
    a_sorted = np.sort(values)[::-1]
    a_inds_sorted = np.argsort(values)[::-1]
    j = a_inds_sorted[0]
    a_j = a_sorted[0]
    a_inds = a_inds_sorted[a_sorted > 0]
    a = a_sorted[1:len(a_inds)]
    k_values = np.array([k - j for k in a_inds if k != j])
    a_inv = np.array([inv(a_n, a_j) for a_n in a])
    return find_time(a_j, a, a_inv, k_values) - j
    '''
    # o = np.where(values > 0)[0]
    # a = values[o]
    a_sorted = np.sort(values)[::-1]
    a_inds_sorted = np.argsort(values)[::-1]
    a_inds = a_inds_sorted[a_sorted > 0]
    a = a_sorted[1:len(a_inds)]
    return find_time_marie_method(a, a_inds)
    '''


def inv(a_i, m):
    m0 = m
    y = 0
    x = 1
    if m == 1:
        return 0
    while a_i > 1:
        # q is quotient
        q = a_i // m
        t = m
        # m is remainder now, process
        # same as Euclid's algo
        m = a_i % m
        a_i = t
        t = y
        # Update x and y
        y = x - q * y
        x = t

        # Make x positive
    if x < 0:
        x = x + m0
    return x


def find_time(a_0, a, a_inv, a_inds):
    i = 0
    max_a_ind = np.argmax(a)
    time = get_time_for_start_point(i, a_0, a, a_inv, a_inds, max_a_ind)
    while time < 0:
        i += 1
        time = get_time_for_start_point(i, a_0, a, a_inv, a_inds, max_a_ind)

    return time


def find_matching_term(current_t, a_0, a_n, a_n_inv, n):
    if not (current_t + n) % a_n == 0:
        return -1
    sub_term = (current_t + n) / a_n
    if not (sub_term - n * a_n_inv) % a_0 == 0:
        return -1
    return (sub_term - n * a_n_inv) / a_0


def get_time_for_start_point(i, a_0, a, a_inv, a_inds, max_a_ind):
    current_t = a[max_a_ind] * (a_inv[max_a_ind] * a_inds[max_a_ind] + a_0 * i) - a_inds[max_a_ind]
    for n in range(len(a)):
        if n == max_a_ind:
            continue
        matching_j = find_matching_term(current_t, a_0, a[n], a_inv[n], a_inds[n])
        if matching_j < 0:
            return -1
    return current_t


def find_time_period_offset(a_j, a, a_inv, a_inds):
    pos = []
    for i in range(len(a)):
        a_jk = a[i]
        a_jk_inv = a_inv[i]
        k = a_inds[i]
        p, o = calculate_period_and_offset(a_jk, a_j, a_jk_inv, k)
        pos.append((p, o, k))

    i = 0
    num_matched = 0
    period, offset, k = pos[0]
    current_time = period * i + offset - k
    while True:
        if check_match(current_time, pos):
            return current_time
        i += 1
        current_time = period * i + offset - k


def check_match(ct, pos):
    for i in range(len(pos)):
        period, offset, k = pos[i]
        if (ct - offset + k) % period != 0:
            return i - 1
    return True


def calculate_period_and_offset(a_jk, a_j, a_jk_inv, k):
    return a_jk * a_j, a_jk_inv * k * a_jk - k


def calculate_with_period(a, offset):
    a_0 = a[0]
    o = offset[0]
    new_as = []
    new_offsets = []
    for i in range(1, len(a)):
        a_i = a[i]
        a_i_inv = inv(a_i, a_0)
        new_a, new_o = calculate_period_and_offset(a_i, a_0, a_i_inv, offset[i] - o)
        new_as.append(new_a)
        new_offsets.append(new_o)
    return calc(new_as, new_offsets)


def calc(a, o):
    if len(a) == 1:
        return a[0], o[0]
    a_0 = a[0]
    o_0 = o[0]
    new_a = []
    new_o = []
    for i in range(1, len(a)):
        a_i = a[i]
        o_i = o[i]
        a_i_inv = inv(a_i, a_0)
        period = a_0 * a_i
        offset = np.mod(a_i_inv * (o_0 - o_i), a_0)
        new_a.append(period)
        new_o.append(offset)
    return calc(new_a, new_o)


def find_time_marie_method(a, k):
    t = a[0]
    i = 1
    step = a[0]
    while i < len(a):
        print(i)
        delta = (t - k[i]) % a[i]
        pos = (t+k[i]-delta) % step
        n = (inv(pos, step) * delta) % step
        t += step*n
        step = step*a[i]
        i += 1
    return t


def q(n, a, k, start=0):
    if n == len(a) - 1:
        return start
    a_n_inv = inv(a[n], a[n + 1])
    return a_n_inv * k[n] + a[n + 1] * q(n + 1, a, k, start=start)


if __name__ == '__main__':
    main('test-input.txt', part1, part2)
