def part1(input: str) -> int:
    entries = parse(input)

    count = 0
    for i in range(len(entries)):
        outputs = entries[i][1]
        for pattern in outputs:
            if len(pattern) in [2, 3, 4, 7]:
                count += 1

    return count


def part2(input: str) -> int:
    entries = parse(input)

    input_entries = [entries[i][0] for i in range(len(entries))]
    output_entries = [entries[i][1] for i in range(len(entries))]

    sum_outputs = 0
    for i in range(len(input_entries)):
        translation = deduction(input_entries[i])

        sum_outputs += int(
            "".join(
                [translate_digits(translation, entry) for entry in output_entries[i]]
            )
        )

    return sum_outputs


def translate_digits(translation_dict: dict, randomized_entry: str) -> str:
    correct_letters = "".join(
        sorted([translation_dict[letter] for letter in randomized_entry])
    )

    letter_to_digit_dict = {
        "abcefg": "0",
        "cf": "1",
        "acdeg": "2",
        "acdfg": "3",
        "bcdf": "4",
        "abdfg": "5",
        "abdefg": "6",
        "acf": "7",
        "abcdefg": "8",
        "abcdfg": "9",
    }

    return letter_to_digit_dict[correct_letters]


def deduction(input_entries: list):
    """
    Deduct which letter stands for which segment:
        1. Find the input representing '1'. Its letters are possibilities for segment 'c' and 'f'.
        2. Find the input representing '7'. It is defined by three letters. The letter which is not a possibility for
         segment 'c' or 'f' is the only possibility for segment 'a'.
        3. Find the input representing '4'. It is defined by four letters. Two of those letters are the letters for '1',
         but the other two letters are the possiblities for segment 'b' and 'd'.
        4. Find the input representing '0', '6' or '9' in any order. They are defined by all but one segment. This means
         the missing letter is the fitting letter for the segment which the number does not define.
    """
    input_entries = list(
        sorted(
            list(filter(lambda input_entry: len(input_entry) != 5, input_entries)),
            key=len,
        )
    )
    all_letters = set([letter for letter in "abcdefg"])

    # dict of possible randomized letters for each segment
    letter_possibilities = {
        "a": all_letters.copy(),
        "b": all_letters.copy(),
        "c": all_letters.copy(),
        "d": all_letters.copy(),
        "e": all_letters.copy(),
        "f": all_letters.copy(),
        "g": all_letters.copy(),
    }

    # '1'
    entry = input_entries[0]
    letter_possibilities["c"] = set(entry)
    letter_possibilities["f"] = set(entry)

    remove_option(letter_possibilities, ["c", "f"], set(entry))

    # '7'
    entry = input_entries[1]
    letter_possibilities["a"] = set(entry).difference(letter_possibilities["c"])

    remove_option(letter_possibilities, ["a"], letter_possibilities["a"])

    # '4'
    entry = input_entries[2]
    possible_set = set(entry).difference(letter_possibilities["c"])
    letter_possibilities["b"] = possible_set.copy()
    letter_possibilities["d"] = possible_set.copy()

    remove_option(letter_possibilities, ["b", "d"], possible_set)

    # '0', '6' and '9'
    for i in [3, 4, 5]:
        entry = input_entries[i]
        segment_set = all_letters.difference(set(entry))

        # missing segment c
        if len(segment_set.intersection(letter_possibilities["c"])) == 1:
            letter_to_set = "c"
        # missing segment e
        elif len(segment_set.intersection(letter_possibilities["e"])) == 1:
            letter_to_set = "e"
        else:  # missing segment d
            letter_to_set = "d"

        letter_possibilities[letter_to_set] = segment_set

        remove_option(letter_possibilities, [letter_to_set], segment_set)

    return {list(v)[0]: k for k, v in letter_possibilities.items()}


def remove_option(possible_letters: dict, keys_to_filter: list, value_to_filter: set):
    for letter in possible_letters.keys():
        if all([letter != key for key in keys_to_filter]):
            possible_letters[letter] = possible_letters[letter].difference(
                value_to_filter
            )


def parse(input: str):
    data = input.splitlines()
    data = [
        [[pattern for pattern in part.split()] for part in entry.split("|")]
        for entry in data
    ]

    return data
