from collections import deque


from aoc.aoc2019.intcode.operation import (
    AdjustRelativeBase,
    Operation,
    Halt,
    Add,
    Mult,
    ReadIn,
    WriteOut,
    JumpIfTrue,
    JumpIfFalse,
    LessThan,
    Equals,
)
from aoc.aoc2019.intcode.parameter import (
    Parameter,
    Position,
    Immediate,
    Relative,
)

from aoc.aoc2019.intcode.ip import InstructionPointer
from aoc.aoc2019.intcode.relative_base import RelativeBase
from aoc.aoc2019.intcode.state import ExecutionState
from aoc.aoc2019.intcode.memory import Memory


class Intcode:
    def __init__(
        self,
        program: list[int],
        inputs: deque[int] = None,
        outputs: deque[int] = None,
    ):
        self.memory = Memory(program)
        self.ip = InstructionPointer()
        self.relative_base = RelativeBase()
        self.state = ExecutionState.INITIAL
        self.inputs = inputs if inputs is not None else deque()
        self.outputs = outputs if outputs is not None else deque()

    def run(self):
        allowed_states = (ExecutionState.INITIAL, ExecutionState.PAUSED)
        if self.state not in allowed_states:
            raise Exception(
                f"Can only start intcode if current state is one of {allowed_states}, but current state is {self.state}"
            )

        self.state = ExecutionState.RUNNING
        while self.state == ExecutionState.RUNNING:
            self._execute_cycle()

    def add_input(self, value: int):
        self.inputs.append(value)

    def get_latest_output(self) -> int:
        return self.outputs[-1]

    def _execute_cycle(self):
        operation = self.parse_instruction()
        self._execute_operation(operation)

    def parse_instruction(self) -> Operation:
        def parse_instruction_parts() -> tuple[tuple[int], int]:
            instruction = str(self.memory[self.ip.value]).zfill(5)
            return (tuple(int(i) for i in instruction[:3][::-1]), int(instruction[3:]))

        modes, opcode = parse_instruction_parts()

        return self._parse_operation(opcode, modes)

    def _parse_operation(self, opcode: int, modes: list[int]) -> Operation:
        match opcode:
            case 99:
                return Halt()
            case 1:
                return Add(*self._parse_parameters(modes, 3))
            case 2:
                return Mult(*self._parse_parameters(modes, 3))
            case 3:
                return ReadIn(*self._parse_parameters(modes, 1), self.inputs)
            case 4:
                return WriteOut(*self._parse_parameters(modes, 1), self.outputs)
            case 5:
                return JumpIfTrue(*self._parse_parameters(modes, 2), self.ip)
            case 6:
                return JumpIfFalse(*self._parse_parameters(modes, 2), self.ip)
            case 7:
                return LessThan(*self._parse_parameters(modes, 3))
            case 8:
                return Equals(*self._parse_parameters(modes, 3))
            case 9:
                return AdjustRelativeBase(
                    *self._parse_parameters(modes, 1), self.relative_base
                )
            case _ as unknown:
                raise Exception(f"unknown operation: {unknown}")

    def _parse_parameters(self, modes: list[int], amount: int) -> list[Parameter]:
        def parse_parameter(mode: int, value: int) -> Parameter:
            match mode:
                case 0:
                    return Position(value)
                case 1:
                    return Immediate(value)
                case 2:
                    return Relative(value, self.relative_base.value)
                case _:
                    raise Exception(f"unknown parameter mode {mode}")

        return [
            parse_parameter(mode, value)
            for value, mode in zip(
                self.memory[self.ip.value + 1 : self.ip.value + 1 + amount], modes
            )
        ]

    def _execute_operation(self, operation: Operation):
        next_state, offset = operation.execute(self.memory)
        self.ip.increment(offset)
        self.state = next_state
