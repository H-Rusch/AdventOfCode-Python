from collections import defaultdict


def part1(input: str) -> int:
    box_ids = parse(input)

    two, three = 0, 0

    for id_num in box_ids:
        has_two, has_three = check_id_number(id_num)
        two = two + 1 if has_two else two
        three = three + 1 if has_three else three

    return two * three


def check_id_number(id_number: str) -> tuple:
    letter_count = count_letters(id_number)
    return 2 in letter_count.values(), 3 in letter_count.values()


def count_letters(id_number: str) -> dict:
    letter_count = defaultdict(int)
    for letter in id_number:
        letter_count[letter] += 1
    return letter_count


def part2(input: str) -> str:
    box_ids = parse(input)

    substrings = dict()

    def create_substring(box_id: str, index: int) -> str:
        if (box_id, index) in substrings:
            return substrings[(box_id, index)]

        substring = box_id[:index] + box_id[index + 1:]
        substrings[(box_id, index)] = substring

        return substring

    for i in range(len(box_ids[0])):
        for first in box_ids:
            first_sub = create_substring(first, i)

            for second in box_ids:
                if first == second:
                    continue

                second_sub = create_substring(second, i)

                if first_sub == second_sub:
                    return first_sub


def parse(input):
    return [line.strip() for line in input.splitlines()]
