Grid = dict[(int, int), str]

MAS = "MAS"

xmas_checks = [
    # horizontal
    ((1, 0), (2, 0), (3, 0)),
    ((-1, 0), (-2, 0), (-3, 0)),
    # vertical
    ((0, 1), (0, 2), (0, 3)),
    ((0, -1), (0, -2), (0, -3)),
    # diagonal
    ((1, 1), (2, 2), (3, 3)),
    ((1, -1), (2, -2), (3, -3)),
    ((-1, 1), (-2, 2), (-3, 3)),
    ((-1, -1), (-2, -2), (-3, -3)),
]


def part1(input: str) -> int:
    grid = parse(input)

    return sum([count_xmas(grid, x, y) for (x, y), ch in grid.items() if ch == "X"])


def part2(input: str) -> int:
    pass


def count_xmas(grid: Grid, x: int, y: int) -> int:
    return len(list(filter(lambda x: x == MAS, find_xmas(grid, x, y))))


def find_xmas(grid: Grid, x: int, y: int) -> list[str]:
    return [
        "".join(
            [
                grid.get((x + x1, y + y1), ""),
                grid.get((x + x2, y + y2), ""),
                grid.get((x + x3, y + y3), ""),
            ]
        )
        for (x1, y1), (x2, y2), (x3, y3) in xmas_checks
    ]


def parse(input: str) -> Grid:
    return {
        (x, y): ch
        for y, line in enumerate(input.splitlines())
        for x, ch in enumerate(line)
    }
