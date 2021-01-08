from shared import main


def alter_program(instructions):
    for position in range(len(instructions)):
        line = instructions[position].split(' ')
        if line[0] == 'jmp':
            altered_instructions = instructions.copy()
            altered_instructions[position] = altered_instructions[position].replace('jmp', 'nop')
            acc, suc = execute_program(altered_instructions)
            if suc:
                return acc
        if line[0] == 'nop':
            altered_instructions = instructions.copy()
            altered_instructions[position] = altered_instructions[position].replace('nop', 'jmp')
            acc, suc = execute_program(altered_instructions)
            if suc:
                return acc
    return -1


def execute_program(instructions):
    accumulator = 0
    position = 0
    lines_executed = []

    while True:
        if position in lines_executed:
            success = False
            break
        if position == len(instructions):
            success = True
            break
        line = instructions[position].split(' ')
        lines_executed.append(position)
        if line[0] == 'acc':
            if line[1][0] == '+':
                accumulator += int(line[1][1:])
            else:
                accumulator -= int(line[1][1:])
            position += 1
        if line[0] == 'nop':
            position += 1

        if line[0] == 'jmp':
            if line[1][0] == '+':
                position += int(line[1][1:])
            else:
                position -= int(line[1][1:])

    return accumulator, success


def preprocess(data_input):
    return data_input.strip().strip().split('\n')


def part1(data_input):
    instructions = preprocess(data_input)
    return execute_program(instructions)[0]


def part2(data_input):
    instructions = preprocess(data_input)
    return alter_program(instructions)


if __name__ == '__main__':
    main('input.txt', part1, part2)
