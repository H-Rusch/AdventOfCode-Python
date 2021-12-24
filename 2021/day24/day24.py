with open("input.txt", 'r') as file:
    batches = file.read().split("inp w\n")
    for num, batch in enumerate(batches):
        CHECK, OFFSET = None, None
        for i, inst in enumerate(batch.splitlines()):
            if i == 4:
                CHECK = inst.split()[-1]

            if i == 14:
                OFFSET = inst.split()[-1]

        if CHECK is not None:
            print(num - 1, CHECK, OFFSET)

# with this information and the beautiful walkthrough by github.com/dphilipson/ the solution can be deducted by hand
# link to the walkthrough: https://github.com/dphilipson/advent-of-code-2021/blob/master/src/days/day24.rs

print(f"Part 1: The biggest accepted model number is {91297395919993}.")

print(f"Part 2: The smallest accepted model number is {71131151917891}.")
