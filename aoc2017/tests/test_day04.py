from ..solutions import day04
from .get_examples.load import load_example


def test_no_repeats():
    assert day04.no_repeats(["aa", "bb", "cc", "dd", "ee"])
    assert not day04.no_repeats(["aa", "bb", "cc", "dd", "aa"])
    assert day04.no_repeats(["aa", "bb", "cc", "dd", "aaa"])


def test_no_anagrams():
    assert day04.no_anagrams(["abcde", "fghij"])
    assert not day04.no_anagrams(["abcde", "xyz", "ecdab"])
    assert day04.no_anagrams(["a", "ab", "abd", "abf", "abj"])
    assert day04.no_anagrams(["iiii", "oiii", "oooi", "oooo"])
    assert not day04.no_anagrams(["oiii", "ioii", "iiio", "iioi"])


def test_part2_combined_example():
    input = load_example("day04.txt")

    assert 3 == day04.part2(input)
