import time


def part1(numbers: list) -> str:
    for _ in range(100):
        new_numbers = numbers[:]
        for i in range(len(numbers)):
            pattern = generate_pattern(i)
            number = 0
            for j, v in enumerate(numbers):
                number += v * pattern[j % len(pattern)]
            new_numbers[i] = (abs(number) % 10)

        numbers = new_numbers

    return "".join([str(n) for n in numbers[:8]])


def part2(numbers: list) -> str:
    offset = int("".join(str(n) for n in numbers[:7]))
    numbers = (numbers * 10000)[offset:]

    for _ in range(100):
        summed_from_index = numbers[-1]
        for i in range(len(numbers) - 2, -1, -1):
            numbers[i] = summed_from_index = (summed_from_index + numbers[i]) % 10

    return "".join([str(n) for n in numbers][:8])


def generate_pattern(index: int) -> list:
    pattern = [n for n in [0, 1, 0, -1] for _ in range(index + 1)]
    pattern.append(pattern.pop(0))

    return pattern


def parse(input):
    with open("input.txt", "r") as file:
        return [int(n) for n in file.read()]


if __name__ == "__main__":
    number_list = parse(input)

    print(f"Part 1: The first eight digits after 100 iterations are {part1(number_list)}.")

    print(f"Part 2: The eight-digit message embedded in the final output list is {part2(number_list)}.")
