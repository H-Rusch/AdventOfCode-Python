class Layer:
    def __init__(self, depth: int, range: int) -> None:
        self.depth = depth
        self.range = range

        self.p = self.range - 1

    def position_at(self, t: int) -> int:
        # the layer's position can be found by modeling it after a triangle wave:
        # https://en.wikipedia.org/wiki/Triangle_wave
        return self.p - abs(t % (2 * self.p) - self.p)

    def severity(self) -> int:
        return self.depth * self.range


def part1(input):
    layers = parse(input)

    return sum(
        [layer.severity() for t, layer in layers.items() if layer.position_at(t) == 0]
    )


def part2(input):
    layers = parse(input)

    delay = 0
    while caught_after_delay(layers, delay):
        delay += 1

    return delay


def caught_after_delay_but_slower(layers: dict[int, Layer], delay: int) -> bool:
    return any([layer.position_at(t + delay) == 0 for t, layer in layers.items()])


def caught_after_delay(layers: dict[int, Layer], delay: int) -> bool:
    # 10 times faster than the above solution
    for t, layer in layers.items():
        if layer is None:
            continue
        if layer.position_at(t + delay) == 0:
            return True

    return False


def parse(input: str) -> dict[int, Layer]:
    layers = {}
    for line in input.splitlines():
        depth, range = map(int, line.split(": "))
        layers[depth] = Layer(depth, range)

    return layers
