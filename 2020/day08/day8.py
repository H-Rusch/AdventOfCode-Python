def run_instructions(instructions, false_output):
    accumulator = 0
    # shows where we are in the instructions
    program_counter = 0
    executed_instructions = []

    while program_counter < len(instructions):
        if program_counter in executed_instructions:
            if false_output:
                print("Value before an instruction is executed a 2nd time is: " + str(accumulator))
            return False
        # get the instruction which should be executed and extract the argument
        instruction = instructions[program_counter]
        arg = int(instruction[5:])
        if instruction[4] == "-":
            arg = -arg
        instruction = instruction[:3]

        # add the executed instruction's index to the list
        executed_instructions.append(program_counter)

        # handle different instructions
        if instruction == "nop":
            program_counter += 1
        elif instruction == "acc":
            accumulator += arg
            program_counter += 1
        else:
            program_counter += arg

    print("Booted Up! Value of accumulator is: " + str(accumulator))
    return True


def change_instructions(instructions):
    # go through each instruction and change the instruction type. Try booting up with those instructions
    for i in range(len(instructions)):
        original_inst = instructions[i]
        if original_inst.startswith("nop", 0, 3):
            instructions[i] = "jmp" + original_inst[3:]
            # try running those instructions
            if run_instructions(instructions, False):
                break
        elif original_inst.startswith("jmp", 0, 3):
            instructions[i] = "nop" + original_inst[3:]
            # try running those instructions
            if run_instructions(instructions, False):
                break
        # change the instruction back and move forward
        instructions[i] = original_inst


# read in instructions
file = open("input.txt", "r")
instruction_list = file.read().split("\n")
file.close()

# part 1
run_instructions(instruction_list, True)
# part 2
change_instructions(instruction_list)
