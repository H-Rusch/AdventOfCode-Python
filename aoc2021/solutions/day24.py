def part1(input: str):
    print_numbers_for_manual_solution(input)

    return 91297395919993


def part2(input: str):
    print_numbers_for_manual_solution(input)

    return 71131151917891


# with this information and the beautiful walkthrough by github.com/dphilipson/ the solution can be deducted by hand
# link to the walkthrough: https://github.com/dphilipson/advent-of-code-2021/blob/master/src/days/day24.rs
def print_numbers_for_manual_solution(input: str):
    batches = input.split("inp w\n")
    for num, batch in enumerate(batches):
        CHECK, OFFSET = None, None
        for i, inst in enumerate(batch.splitlines()):
            if i == 4:
                CHECK = inst.split()[-1]

            if i == 14:
                OFFSET = inst.split()[-1]

        if CHECK is not None:
            print(num - 1, CHECK, OFFSET)
