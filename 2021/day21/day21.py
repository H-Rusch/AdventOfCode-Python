from functools import cache


def part_1(start1: int, start2: int) -> int:
    pos1, pos2, score1, score2 = start1, start2, 0, 0
    turn = 0
    dice_value = 1
    roll_number = 0

    while True:
        if turn % 2 == 0:
            pos1, dice_value, roll_number = iterate(pos1, dice_value, roll_number)
            score1 += pos1
            if score1 >= 1000:
                return score2 * roll_number
        else:
            pos2, dice_value, roll_number = iterate(pos2, dice_value, roll_number)
            score2 += pos2
            if score2 >= 1000:
                return score1 * roll_number

        turn = (turn + 1) % 2


def iterate(position: int, dice_value: int, roll_number: int) -> tuple:
    rolled = 0
    for i in range(3):
        rolled += dice_value
        dice_value = (dice_value + 1) % 100
        if dice_value == 0:
            dice_value = 100

    position += rolled
    position = position % 10
    if position == 0:
        position = 10

    return position, dice_value, roll_number + 3


def part_2(start1: int, start2: int) -> int:
    wins1, wins2 = play_from_state(start1, start2, 0, 0)

    return max((wins1, wins2))


@cache
def play_from_state(this_position: int, other_position: int, this_score: int, other_score: int) -> tuple:
    if this_score >= 21:
        return 1, 0
    if other_score >= 21:
        return 0, 1

    total_wins_this, total_wins_other = 0, 0

    for i in [1, 2, 3]:
        for j in [1, 2, 3]:
            for k in [1, 2, 3]:
                new_position = (i + j + k + this_position) % 10
                if new_position == 0:
                    new_position = 10
                new_score = this_score + new_position

                other_wins, this_wins = play_from_state(other_position, new_position, other_score, new_score)

                total_wins_this += this_wins
                total_wins_other += other_wins

    return total_wins_this, total_wins_other


if __name__ == "__main__":
    start1, start2 = 9, 4

    print(f"Part 1: The score of the losing player multiplied by the number of times the dice was rolled is "
          f"{part_1(start1, start2)}.")

    print(f"Part 2: The player who wins in more universes wins in {part_2(start1, start2)} universes.")
