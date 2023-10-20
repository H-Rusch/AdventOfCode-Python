from dataclasses import dataclass
from collections import defaultdict
import re


PARTICLE_PATTERN = re.compile(
    r"p=<(-?\d+,-?\d+,-?\d+)>, v=<(-?\d+,-?\d+,-?\d+)>, a=<(-?\d+,-?\d+,-?\d+)>"
)


@dataclass
class Particle:
    id: int
    coordinate: list[int]
    velocity: list[int]
    acceleration: list[int]

    def update(self):
        for i in range(3):
            self.velocity[i] += self.acceleration[i]
            self.coordinate[i] += self.velocity[i]

    def manhatten_distance(self):
        x, y, z = self.coordinate
        return abs(x) + abs(y) + abs(z)


def part1(input):
    particles = parse(input)

    particles.sort(
        key=lambda particle: (
            sum(abs(a) for a in particle.acceleration),
            sum(abs(v) for v in particle.velocity),
            particle.manhatten_distance(),
        )
    )

    return particles[0].id


def part2(input):
    particles = parse(input)

    # simulate a high number of times after which all collisions (should) have happened
    for _ in range(1_000):
        simulate_rount(particles)

    return len(particles)


def simulate_rount(particles: list):
    for particle in particles:
        particle.update()

    positions = defaultdict(list)
    for particle in particles:
        positions[tuple(particle.coordinate)].append(particle)

    particles.clear()
    for values in positions.values():
        if len(values) == 1:
            particles.extend(values)


def parse(input: str) -> list[Particle]:
    particles = []
    for i, line in enumerate(input.splitlines()):
        groups = PARTICLE_PATTERN.match(line).groups()
        coordinate = [int(n) for n in groups[0].split(",")]
        velocity = [int(n) for n in groups[1].split(",")]
        acceleration = [int(n) for n in groups[2].split(",")]

        particles.append(Particle(i, coordinate, velocity, acceleration))

    return particles
