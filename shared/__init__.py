def main(input_file, f1, f2):
    with open(input_file, 'r') as f:
        di = f.read()
        print('Part 1: {}'.format(f1(di)))
        print('Part 2: {}'.format(f2(di)))