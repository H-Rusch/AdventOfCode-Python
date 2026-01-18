def part1(input):
    passphrases = parse(input)

    valid_phrases = list(filter(no_repeats, passphrases))

    return len(valid_phrases)


def part2(input):
    passphrases = parse(input)

    valid_phrases = list(filter(no_anagrams, passphrases))

    return len(valid_phrases)


def no_repeats(passphrase: list[str]) -> bool:
    return len(passphrase) == len(set(passphrase))


def no_anagrams(passphrase: list[str]) -> bool:
    passphrase = ["".join(sorted(word)) for word in passphrase]

    return no_repeats(passphrase)


def parse(input: str) -> list[list[str]]:
    return [line.split() for line in input.splitlines()]
