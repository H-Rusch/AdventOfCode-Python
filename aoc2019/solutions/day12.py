import math
import re


class Moon:
    def __init__(self, x, y, z):
        self.pos = [x, y, z]
        self.vel = [0, 0, 0]

    def apply_all_gravity(self, other):
        for i in range(3):
            self.apply_gravity(other, i)

    def apply_gravity(self, other, index):
        if self.pos[index] > other.pos[index]:
            self.vel[index] -= 1
            other.vel[index] += 1
        elif self.pos[index] < other.pos[index]:
            self.vel[index] += 1
            other.vel[index] -= 1

    def change_all_positions(self):
        for i in range(3):
            self.change_position(i)

    def change_position(self, index):
        self.pos[index] += self.vel[index]

    def calculate_total_energy(self) -> int:
        return sum([abs(v) for v in self.pos]) * sum([abs(v) for v in self.vel])


def part1(input) -> int:
    moons = parse(input)

    for _ in range(1000):
        for i in range(len(moons) - 1):
            for j in range(i + 1, len(moons)):
                moons[i].apply_all_gravity(moons[j])

        for m1 in moons:
            m1.change_all_positions()

    return sum([moon.calculate_total_energy() for moon in moons])


def part2(input) -> int:
    moons = parse(input)

    starting_positions = [moon.pos[:] for moon in moons]

    steps_till_cycle = [0, 0, 0]

    for i in range(3):
        while True:
            for left in range(len(moons) - 1):
                for right in range(left + 1, len(moons)):
                    moons[left].apply_gravity(moons[right], i)
            for moon in moons:
                moon.change_position(i)
            steps_till_cycle[i] += 1

            if all(
                moon.pos[i] == starting_positions[index][i]
                for index, moon in enumerate(moons)
            ) and all(moon.vel[i] == 0 for moon in moons):
                break

    return math.lcm(*steps_till_cycle)


def parse(input):
    moons = []

    for line in input.splitlines():
        x, y, z = re.search("<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line).groups()
        moons.append(Moon(int(x), int(y), int(z)))

    return moons
