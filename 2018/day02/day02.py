from collections import defaultdict


def part_1(box_ids: list) -> int:
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


def part_2(box_ids: list) -> str:
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


def parse_input():
    with open("input.txt", "r") as file:
        return [line.strip() for line in file.readlines()]


if __name__ == "__main__":
    warehouse = parse_input()

    print(f"Part 1: The checksum for the list of box ids is {part_1(warehouse)}.")

    print(f"Part 2: The letters common between the correct box IDs are {part_2(warehouse)}.")
