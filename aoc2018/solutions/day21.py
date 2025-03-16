def part1(_) -> int:
    """Code decompiled from input. See 'input_decoded.txt'."""
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


def part2(_) -> int:
    """Code decompiled from input. See 'input_decoded.txt'."""
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
