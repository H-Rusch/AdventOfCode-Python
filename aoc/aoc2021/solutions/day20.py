def part1(input: str) -> int:
    algorithm, coordinates = parse(input)

    return enhance_loop(algorithm, coordinates.copy(), 2)


def part2(input: str) -> int:
    algorithm, coordinates = parse(input)

    return enhance_loop(algorithm, coordinates.copy(), 50)


def enhance_loop(algorithm: list, img_coordinates: set, iterations: int) -> int:
    for i in range(iterations):
        if i % 2 == 0:
            background = 0
        else:
            background = 1

        next_step = set()

        start_x = min(img_coordinates, key=lambda c: c[0])[0]
        end_x = max(img_coordinates, key=lambda c: c[0])[0]
        start_y = min(img_coordinates, key=lambda c: c[1])[1]
        end_y = max(img_coordinates, key=lambda c: c[1])[1]

        for x in range(start_x - 1, end_x + 3):
            for y in range(start_y - 1, end_y + 3):
                coordinate = (x, y)
                binary = get_binary(
                    coordinate,
                    img_coordinates,
                    start_x,
                    end_x,
                    start_y,
                    end_y,
                    background,
                )

                symbol = algorithm[int(binary, 2)]
                if symbol == "#":
                    next_step.add(coordinate)
        img_coordinates = next_step

    # print_image(img_coordinates)  # to visualize the image
    return len(img_coordinates)


def get_binary(
    coordinate: tuple,
    img_coordinates: set,
    start_x: int,
    end_x: int,
    start_y: int,
    end_y: int,
    background: int,
) -> str:
    binary = ""
    for x, y in get_adjacent(coordinate):
        if x < start_x or x > end_x or y < start_y or y > end_y:
            if background == 1:
                binary += "1"
            else:
                binary += "0"

        else:
            if (x, y) in img_coordinates:
                binary += "1"
            else:
                binary += "0"

    return binary


def print_image(img_coordinates: set):
    start_x = min(img_coordinates, key=lambda c: c[0])[0]
    end_x = max(img_coordinates, key=lambda c: c[0])[0]
    start_y = min(img_coordinates, key=lambda c: c[1])[1]
    end_y = max(img_coordinates, key=lambda c: c[1])[1]

    for x in range(start_x - 1, end_x + 2):
        for y in range(start_y - 1, end_y + 2):
            if (x, y) in img_coordinates:
                print("# ", end="")
            else:
                print(". ", end="")
        print()


def get_adjacent(coordinate: tuple) -> list:
    return [
        (coordinate[0] + dx, coordinate[1] + dy)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
    ]


def parse(input: str):
    image_algorithm, img = input.split("\n\n")

    img_coordinates = set()
    img = img.split("\n")
    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i][j] == "#":
                img_coordinates.add((i, j))

    return image_algorithm, img_coordinates
