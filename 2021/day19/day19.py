class Scanner:
    def __init__(self):
        self.beacons = set()
        self.origin = None


class Beacon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.distances = set()

    def apply_delta(self, other: "Beacon") -> "Beacon":
        return Beacon(self.x + other.x, self.y + other.y, self.z + other.z)

    def rotate(self, axis: str) -> "Beacon":
        if axis == "x":
            return Beacon(self.x, self.z, -self.y)
        elif axis == "y":
            return Beacon(-self.z, self.y, self.x)
        elif axis == "z":
            return Beacon(self.y, -self.x, self.z)

    def calculate_distance(self, other: "Beacon") -> int:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2

    def __eq__(self, other: "Beacon") -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"


def both_parts(scanners: list):
    # calculate the distances between the beacons in each scanner
    for scanner in scanners:
        calculate_distances(scanner)

    known = scanners.pop(0)
    finished = [known]
    known.origin = (0, 0, 0)

    while len(scanners) > 0:
        calculate_distances(known)
        for scanner in scanners:
            calculate_distances(scanner)

        for i in range(len(scanners)):
            overlap = count_overlap(known, scanners[i])
            if overlap >= 12:
                candidate = scanners[i]
                index = i
                break

        if transform(known, candidate):
            finished.append(candidate)
            scanners.pop(index)

    max_dist = 0
    for i in range(len(finished)):
        for j in range(i + 1, len(finished)):
            max_dist = max([max_dist, manhatten_distance(finished[i].origin, finished[j].origin)])

    return len(known.beacons), max_dist


def manhatten_distance(t1: tuple, t2: tuple) -> int:
    return abs(t1[0] - t2[0]) + abs(t1[1] - t2[1]) + abs(t1[2] - t2[2])


def transform(known: Scanner, other: Scanner):
    for i in range(6):
        for j in range(4):
            for o in other.beacons:
                for k in known.beacons:
                    delta = Beacon(k.x - o.x, k.y - o.y, k.z - o.z)
                    shift = {u.apply_delta(delta) for u in other.beacons}

                    count = 0
                    for shifting in shift:
                        if shifting in known.beacons:
                            count += 1
                        if count >= 12:
                            for a in shift:
                                known.beacons.add(a)
                            other.origin = (delta.x, delta.y, delta.z)

                            return True

            other.beacons = {o.rotate("x") for o in other.beacons}

        if i < 5:
            if i < 3:
                other.beacons = {o.rotate("y") for o in other.beacons}
            if i > 2 or i == 4:
                other.beacons = {o.rotate("z") for o in other.beacons}

    return False


def calculate_distances(scanner: Scanner):
    for b1 in scanner.beacons:
        for b2 in scanner.beacons:
            if b1 != b2:
                distance = b1.calculate_distance(b2)
                b1.distances.add(distance)
                b2.distances.add(distance)


def count_overlap(scanner1: Scanner, scanner2: Scanner):
    num = 0
    for beacon1 in scanner1.beacons:
        for beacon2 in scanner2.beacons:
            if len(beacon1.distances.intersection(beacon2.distances)) >= 11:
                num += 1

    return num


def parse_input():
    with open("input.txt") as file:
        batches = [batch for batch in file.read().split("\n\n")]
        scanners = []

        for i in range(len(batches)):
            scanners.append(Scanner())

            readings = batches[i].split("\n")
            for reading in readings:
                if reading[1] == "-":
                    continue
                values = list(map(lambda s: int(s), reading.split(",")))
                scanners[i].beacons.add(Beacon(values[0], values[1], values[2]))

    return scanners


if __name__ == "__main__":
    scanner_list = parse_input()

    num_beacons, max_distance = both_parts(scanner_list)

    print(f"Part 1: The number of beacons is {num_beacons}.")

    print(f"Part 2: The maximum distance between beacons is {max_distance}.")
