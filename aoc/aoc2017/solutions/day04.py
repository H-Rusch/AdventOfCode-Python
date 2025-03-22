from typing import List


def part1(input):
    passphrases = parse(input)

    valid_phrases = list(filter(no_repeats, passphrases))

    return len(valid_phrases)


def part2(input):
    passphrases = parse(input)

    valid_phrases = list(filter(no_anagrams, passphrases))

    return len(valid_phrases)


def no_repeats(passphrase: List[str]) -> bool:
    return len(passphrase) == len(set(passphrase))


def no_anagrams(passphrase: List[str]) -> bool:
    passphrase = ["".join(sorted(word)) for word in passphrase]

    return no_repeats(passphrase)


def parse(input: str) -> List[List[str]]:
    return [line.split() for line in input.splitlines()]
