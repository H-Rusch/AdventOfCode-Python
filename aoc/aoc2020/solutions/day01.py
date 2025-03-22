def part1(input):
    numbers = parse(input)

    for i in range(len(numbers) - 1):
        for j in range(i + 1, len(numbers)):
            summ = numbers[i] + numbers[j]
            if summ == 2020:
                return numbers[i] * numbers[j]


def part2(input):
    numbers = parse(input)

    for i in range(len(numbers) - 1):
        for j in range(i + 1, len(numbers)):
            for k in range(j + 1, len(numbers)):
                summ = numbers[i] + numbers[j] + numbers[k]
                if summ == 2020:
                    return numbers[i] * numbers[j] * numbers[k]


def parse(input: str):
    return [int(i) for i in input.splitlines()]
