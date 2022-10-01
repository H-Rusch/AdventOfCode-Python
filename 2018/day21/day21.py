def part_1() -> int:
    """Code decompiled from input. See 'input_decoded.txt'. """
    r4 = 0
    while True:
        r5 = r4 | 65536
        r4 = 10704114
        while True:
            r2 = r5 & 255
            r4 += r2
            r4 &= 16777215
            r4 *= 65899
            r4 &= 16777215

            if 256 > r5:
                return r4
            else:
                r5 = r5 // 256


def part_2() -> int:
    """Code decompiled from input. See 'input_decoded.txt'. """
    seen = set()
    last = 0

    r4 = 0
    while True:
        r5 = r4 | 65536
        r4 = 10704114
        while True:
            r2 = r5 & 255
            r4 += r2
            r4 &= 16777215
            r4 *= 65899
            r4 &= 16777215

            if 256 > r5:
                if r4 in seen:
                    return last
                else:
                    seen.add(r4)
                    last = r4
                    break
            else:
                r5 = r5 // 256


if __name__ == "__main__":
    print(f"Part 1: The lowest value that halts the program is {part_1()}.")

    print(f"Part 2: The lowest value that halt the program after executing the most instructions is {part_2()}.")
