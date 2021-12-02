def part_1():
    global instructions

    horizontal = 0
    vertical = 0

    for instruction in instructions:
        direction, number = instruction.split()

        if direction == "up":
            vertical -= int(number)
        elif direction == "down":
            vertical += int(number)
        else:
            horizontal += int(number)

    print(f"Part 1: The final horizontal position multiplied by the final depth is {str(horizontal * vertical)}.")


def part_2():
    global instructions

    horizontal = 0
    vertical = 0
    aim = 0

    for instruction in instructions:
        direction, number = instruction.split()

        if direction == "up":
            aim -= int(number)
        elif direction == "down":
            aim += int(number)
        else:
            horizontal += int(number)
            vertical += aim * int(number)

    print(f"Part 1: The final horizontal position multiplied by the final depth is {str(horizontal * vertical)}.")


if __name__ == "__main__":
    with open("input.txt", 'r', encoding='utf-8') as file:
        instructions = [s for s in file.read().splitlines()]

        part_1()

        part_2()
