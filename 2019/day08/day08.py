WIDTH = 25
HEIGHT = 6
LAYER_SIZE = WIDTH * HEIGHT


def part_1(image_layers: list) -> int:
    # here I chose an approach with iterationg over the values once and memorizing the layer with the least amount of
    # zeros in order to save computing time
    minimum_zeros = LAYER_SIZE
    layer_with_min_zeros = None
    for layer in image_layers:
        if layer.count(0) < minimum_zeros:
            minimum_zeros = layer.count(0)
            layer_with_min_zeros = layer

    return layer_with_min_zeros.count(1) * layer_with_min_zeros.count(2)


def part_2(image_layers: list):
    visibible_image = [get_value_at_index(i, image_layers) for i in range(LAYER_SIZE)]

    for y in range(HEIGHT):
        print("".join(["█ " if n == 1 else "  " for n in visibible_image[y * WIDTH: (y + 1) * WIDTH]]))


def get_value_at_index(index: int, image_layers: list) -> int:
    for layer in image_layers:
        if layer[index] == 0 or layer[index] == 1:
            return layer[index]

    return -1


def parse_input():
    with open("input.txt", "r") as file:
        image = file.read()
        layers = [image[i * LAYER_SIZE: (i + 1) * LAYER_SIZE] for i in range(len(image) // LAYER_SIZE)]
        return [[int(d) for d in layer] for layer in layers]


if __name__ == "__main__":
    layer_list = parse_input()

    print(f"Part 1: The number of 1s * the number of 2s in the layer with the fewest 0s is {part_1(layer_list)}.")

    print(f"Part 2: The transmitted image is:")
    part_2(layer_list)
