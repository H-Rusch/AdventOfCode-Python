WIDTH = 25
HEIGHT = 6
LAYER_SIZE = WIDTH * HEIGHT


def part1(input) -> int:
    layers = parse(input)
    # here I chose an approach with iterating over the values once and memorizing the layer with the least amount of
    # zeros in order to save computing time
    minimum_zeros = LAYER_SIZE
    layer_with_min_zeros = None
    for layer in layers:
        if layer.count(0) < minimum_zeros:
            minimum_zeros = layer.count(0)
            layer_with_min_zeros = layer

    return layer_with_min_zeros.count(1) * layer_with_min_zeros.count(2)


def part2(input) -> int:
    layers = parse(input)

    visible_image = [get_value_at_index(i, layers) for i in range(LAYER_SIZE)]

    for y in range(HEIGHT):
        print(
            "".join(
                [
                    "█ " if n == 1 else "  "
                    for n in visible_image[y * WIDTH : (y + 1) * WIDTH]
                ]
            )
        )


def get_value_at_index(index: int, image_layers: list) -> int:
    for layer in image_layers:
        if layer[index] == 0 or layer[index] == 1:
            return layer[index]

    return -1


def parse(input):
    layers = [
        input[i * LAYER_SIZE : (i + 1) * LAYER_SIZE]
        for i in range(len(input) // LAYER_SIZE)
    ]
    return [[int(d) for d in layer] for layer in layers]
