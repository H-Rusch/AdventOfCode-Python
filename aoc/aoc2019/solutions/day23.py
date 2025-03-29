from aoc.aoc2019.intcode.intcode import Intcode


def part1(input) -> int:
    instructions = parse(input)

    computers = []
    for i in range(50):
        computer = Intcode(instructions)
        computer.add_input(i)
        computers.append(computer)

    while True:
        for computer in computers:
            if len(computer.inputs) == 0:
                computer.add_input(-1)

            computer.run()
            while len(computer.outputs) >= 3:
                adr, x, y = (computer.outputs.popleft() for _ in range(3))

                if adr == 255:
                    return y

                computers[adr].inputs.extend([x, y])


def part2(input) -> int:
    instructions = parse(input)

    computers = []
    nat_x, nat_y = None, None
    last_delivered_y = None

    for i in range(50):
        computer = Intcode(instructions)
        computer.add_input(i)
        computers.append(computer)

    while True:
        all_idle = True
        for computer in computers:
            if len(computer.inputs) == 0:
                computer.add_input(-1)

            computer.run()
            while len(computer.outputs) >= 3:
                adr, x, y = (computer.outputs.popleft() for _ in range(3))

                if adr == 255:
                    nat_x, nat_y = x, y
                else:
                    computers[adr].inputs.extend([x, y])
                    all_idle = False

        if all_idle:
            if nat_y is None:
                continue
            computers[0].inputs.extend([nat_x, nat_y])
            if last_delivered_y == nat_y:
                return nat_y
            last_delivered_y = nat_y


def parse(input):
    return [int(n) for n in input.split(",")]
