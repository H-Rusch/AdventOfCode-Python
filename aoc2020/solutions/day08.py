def part1(input):
    return run_instructions(input.splitlines())[1]

def part2(input):
    instructions = input.splitlines()
    change_instructions(instructions)

    return run_instructions(instructions)[1]


def run_instructions(instructions) -> (bool, int):
    accumulator = 0
    # shows where we are in the instructions
    program_counter = 0
    executed_instructions = set()

    while program_counter < len(instructions):
        if program_counter in executed_instructions:
            return (False, accumulator)
        # get the instruction which should be executed and extract the argument
        instruction = instructions[program_counter]
        arg = int(instruction[5:])
        if instruction[4] == "-":
            arg = -arg
        instruction = instruction[:3]

        # add the executed instruction's index to the list
        executed_instructions.add(program_counter)

        # handle different instructions
        match instruction:
            case "nop": 
                program_counter += 1
            case "acc":
                program_counter += 1
                accumulator += arg
            case _:
                program_counter += arg

    return (True, accumulator)


def change_instructions(instructions):
    replacements = {"nop": "jmp", "jmp": "nop"}
    # go through each instruction and change the instruction type. Try booting up with those instructions
    for i, original_inst in enumerate(instructions):
        prefix = original_inst[:3]
        if prefix in replacements:
            instructions[i] = replacements[prefix] + original_inst[3:]
            
            # try running those instructions
            if run_instructions(instructions)[0]:
                
                break
        
        # change the instruction back and move forward
        instructions[i] = original_inst
