def part_1(instruction_list: list) -> int:
    horizontal = 0
    vertical = 0

    for instruction in instruction_list:
        direction, number = instruction.split()

        if direction == "up":
            vertical -= int(number)
        elif direction == "down":
            vertical += int(number)
        else:
            horizontal += int(number)

    return horizontal * vertical


def part_2(instruction_list: list) -> int:
    horizontal = 0
    vertical = 0
    aim = 0

    for instruction in instruction_list:
        direction, number = instruction.split()

        if direction == "up":
            aim -= int(number)
        elif direction == "down":
            aim += int(number)
        else:
            horizontal += int(number)
            vertical += aim * int(number)

    return horizontal * vertical


def parse_input():
    with open("input.txt", 'r', encoding='utf-8') as file:
        return [s for s in file.read().splitlines()]


if __name__ == "__main__":
    instructions = parse_input()

    print(f"Part 1: The final horizontal position multiplied by the final depth is {part_1(instructions)}.")

    print(f"Part 2: The final horizontal position multiplied by the final depth is {part_2(instructions)}.")
