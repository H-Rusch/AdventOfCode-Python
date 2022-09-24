import math
import re
import cv2
import numpy as np


class Point:
    def __init__(self, start_x: int, start_y: int, vel_x: int, vel_y: int):
        self.x = start_x
        self.y = start_y
        self.vel_x = vel_x
        self.vel_y = vel_y

    def step(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def reverse_step(self):
        self.x -= self.vel_x
        self.y -= self.vel_y


def part_1(points: list):
    min_density = math.inf

    for i in range(20_000):
        # find out when the points are all 'close' together
        min_x = min([point.x for point in points])
        max_x = max([point.x for point in points])
        min_y = min([point.y for point in points])
        max_y = max([point.y for point in points])

        density = max_x - min_x + max_y - min_y
        if density < min_density:
            min_density = density
        else:
            for point in points:
                point.reverse_step()
            break

        for point in points:
            point.step()

    make_picture(points)


def make_picture(points: list):
    min_x = min([point.x for point in points])
    max_x = max([point.x for point in points])
    min_y = min([point.y for point in points])
    max_y = max([point.y for point in points])

    for point in points:
        point.x = point.x - min_x if min_x > 0 else point.x + min_x
        point.y = point.y - min_y if min_y > 0 else point.y + min_y

    grid = np.zeros((max_y - min_y + 1, max_x - min_x + 1))
    for point in points:
        grid[point.y, point.x] = 255

    cv2.imwrite('grid.png', grid)


def part_2(points: list) -> int:
    min_density = math.inf
    min_density_time = 0

    for i in range(20_000):
        # find out when the points are all 'close' together
        min_x = min([point.x for point in points])
        max_x = max([point.x for point in points])
        min_y = min([point.y for point in points])
        max_y = max([point.y for point in points])

        density = max_x - min_x + max_y - min_y
        if density < min_density:
            min_density = density
            min_density_time = i
        else:
            return min_density_time

        for point in points:
            point.step()


def parse_input():
    with open("input.txt", "r") as file:
        points = []
        for line in file.readlines():
            line = line.replace(" ", "")
            values = [int(d) for d in re.match(r"position=<(-?\d+),(-?\d+)>velocity=<(-?\d+),(-?\d+)", line).groups()]
            points.append(Point(*values))
        return points


if __name__ == "__main__":
    point_list = parse_input()

    print("Part 1: The answer can be seen in the generated file 'grid_png'.")
    part_1(point_list)

    point_list = parse_input()
    print(f"Part 2: The message appears after {part_2(point_list)} seconds.")
