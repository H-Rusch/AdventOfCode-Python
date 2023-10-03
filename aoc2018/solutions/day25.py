class UnionFind:
    def __init__(self, size: int):
        self.parent = [i for i in range(size)]

    def make_set(self, v: int):
        self.parent[v] = v

    def find_set(self, v: int) -> int:
        if v == self.parent[v]:
            return v
        return self.find_set(self.parent[v])

    def union_set(self, v1: int, v2: int):
        a = self.find_set(v1)
        b = self.find_set(v2)
        if a != b:
            self.parent[b] = a


def manhatten_distance(point1, point2) -> int:
    return sum(abs(v[0] - v[1]) for v in zip(point1, point2))


def part1(input: str) -> int:
    points = parse(input)

    uf = UnionFind(len(points))

    for i, p1 in enumerate(points):
        for j, p2 in enumerate(points):
            if j > i:
                if manhatten_distance(p1, p2) <= 3:
                    uf.union_set(i, j)

    clusters = set()
    for i, p in enumerate(points):
        clusters.add(uf.find_set(i))

    return len(clusters)

def part2(_):
    return "No second puzzle ☺️"


def parse(input: str):
    points = []
    for line in input.strip().splitlines():
        points.append(tuple(map(int, line.split(","))))
    return points
