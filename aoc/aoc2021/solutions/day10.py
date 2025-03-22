from collections import deque
import numpy as np


def part1(input: str):
    answer_1, _ = both_parts(input.splitlines())

    return answer_1


def part2(input: str):
    _, answer_2 = both_parts(input.splitlines())

    return answer_2


def both_parts(line_list: list) -> tuple:
    bracket_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
    corrupted_points = {")": 3, "]": 57, "}": 1197, ">": 25137}

    corrupted_score = 0
    incomplete_scores = []

    for line in line_list:
        stack = deque()
        corrupt = False
        for sign in line:
            if sign in ["(", "[", "{", "<"]:
                stack.append(sign)

            else:
                if sign == bracket_pairs[stack[-1]]:
                    stack.pop()

                else:
                    # wrong closing bracket found => line is corrupted
                    corrupted_score += corrupted_points[sign]
                    corrupt = True
                    break

        if not corrupt:
            # no corruption found, but line is incomlete
            completion_string = [bracket_pairs[opening] for opening in reversed(stack)]
            incomplete_scores.append(calculate_incomplete_score(completion_string))

    return corrupted_score, int(np.median(incomplete_scores))


def calculate_incomplete_score(completion_signs: list) -> int:
    incomplete_points = {")": 1, "]": 2, "}": 3, ">": 4}
    score = 0
    for sign in completion_signs:
        score = score * 5 + incomplete_points[sign]

    return score
