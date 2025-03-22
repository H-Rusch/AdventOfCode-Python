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

x_mas_checks = [
    ((-1, -1), (0, 0), (1, 1)),
    ((-1, 1), (0, 0), (1, -1)),
]


def part1(input: str) -> int:
    grid = parse(input)

    return sum([count_xmas(grid, x, y) for (x, y), ch in grid.items() if ch == "X"])


def part2(input: str) -> int:
    grid = parse(input)

    return sum([is_x_mas(grid, x, y) for (x, y), ch in grid.items() if ch == "A"])


def count_xmas(grid: Grid, x: int, y: int) -> int:
    def find_xmas() -> list[str]:
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

    return len(list(filter(lambda x: x == MAS, find_xmas())))


def is_x_mas(grid: Grid, x: int, y: int) -> bool:
    def find_x_mas() -> list[str]:
        return [
            "".join(
                [
                    grid.get((x + x1, y + y1), ""),
                    grid.get((x + x2, y + y2), ""),
                    grid.get((x + x3, y + y3), ""),
                ]
            )
            for (x1, y1), (x2, y2), (x3, y3) in x_mas_checks
        ]

    return all(map(is_mas, find_x_mas()))


def is_mas(s: str) -> bool:
    return s == MAS or s == MAS[::-1]


def parse(input: str) -> Grid:
    return {
        (x, y): ch
        for y, line in enumerate(input.splitlines())
        for x, ch in enumerate(line)
    }
