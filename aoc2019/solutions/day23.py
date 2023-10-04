from .intcode import intcode


def part1(input) -> int:
    instructions = parse(input)

    computers = []
    for i in range(50):
        computer = intcode.IntcodeV3_5(instructions)
        computer.input.append(i)
        computers.append(computer)

    while True:
        for computer in computers:
            computer.execute_program()
            while len(computer.output) >= 3:
                adr, x, y = computer.output[:3]
                computer.output = computer.output[3:]

                if adr == 255:
                    return y
                computers[adr].input.extend([x, y])


def part2(input) -> int:
    instructions = parse(input)

    computers = []
    nat_x, nat_y = None, None
    last_delivered_y = None

    for i in range(50):
        computer = intcode.IntcodeV3_5(instructions)
        computer.input.append(i)
        computers.append(computer)

    while True:
        all_idle = True
        for computer in computers:
            computer.execute_program()
            while len(computer.output) >= 3:
                adr, x, y = computer.output[:3]
                computer.output = computer.output[3:]

                if adr == 255:
                    nat_x, nat_y = x, y
                else:
                    computers[adr].input.extend([x, y])
                    all_idle = False

        if all_idle:
            if nat_y is None:
                continue
            computers[0].input.extend([nat_x, nat_y])
            if last_delivered_y == nat_y:
                return nat_y
            last_delivered_y = nat_y


def parse(input):
    return [int(n) for n in input.split(",")]
