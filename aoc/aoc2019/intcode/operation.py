from collections import deque
from abc import ABC, abstractmethod

from aoc.aoc2019.intcode.ip import InstructionPointer
from aoc.aoc2019.intcode.relative_base import RelativeBase
from aoc.aoc2019.intcode.state import ExecutionState
from aoc.aoc2019.intcode.parameter import Parameter


class Operation(ABC):
    def __init__(self, offset: int, next_state: ExecutionState):
        self.offset = offset
        self.next_state = next_state

    def execute(self, registers: list[int]) -> tuple[ExecutionState, int]:
        result = self._run(registers)
        return result if result is not None else (self.next_state, self.offset)

    @abstractmethod
    def _run(self, registers: list[int]) -> tuple[ExecutionState, int] | None:
        pass

    def _return_value(self) -> tuple[ExecutionState, int]:
        return self.next_state, self.offset


class RunningOperation(Operation):
    def __init__(self, offset: int):
        super().__init__(offset, ExecutionState.RUNNING)


class BinaryOp(RunningOperation):
    def __init__(
        self, param1: Parameter, param2: Parameter, destination: Parameter, op: callable
    ):
        super().__init__(4)
        self.param1 = param1
        self.param2 = param2
        self.destination = destination
        self.op = op

    def _run(self, registers: list[int]):
        val1 = self.param1.get_value(registers)
        val2 = self.param2.get_value(registers)
        registers[self.destination.get_destination()] = self.op(val1, val2)


class ConditionalJump(RunningOperation):
    def __init__(
        self,
        param1: Parameter,
        param2: Parameter,
        ip: InstructionPointer,
        condition: callable,
    ):
        super().__init__(3)
        self.param1 = param1
        self.param2 = param2
        self.ip = ip
        self.condition = condition

    def _run(self, registers: list[int]):
        if self.condition(self.param1.get_value(registers)):
            self.ip.jump(self.param2.get_value(registers))


class Halt(Operation):
    def __init__(self):
        super().__init__(1, ExecutionState.HALTED)

    def _run(self, _):
        pass


class Add(BinaryOp):
    def __init__(self, p1, p2, dest):
        super().__init__(p1, p2, dest, lambda a, b: a + b)


class Mult(BinaryOp):
    def __init__(self, p1, p2, dest):
        super().__init__(p1, p2, dest, lambda a, b: a * b)


class LessThan(BinaryOp):
    def __init__(self, p1, p2, dest):
        super().__init__(p1, p2, dest, lambda a, b: int(a < b))


class Equals(BinaryOp):
    def __init__(self, p1, p2, dest):
        super().__init__(p1, p2, dest, lambda a, b: int(a == b))


class JumpIfTrue(ConditionalJump):
    def __init__(self, p1, p2, ip):
        super().__init__(p1, p2, ip, lambda x: x != 0)


class JumpIfFalse(ConditionalJump):
    def __init__(self, p1, p2, ip):
        super().__init__(p1, p2, ip, lambda x: x == 0)


class ReadIn(RunningOperation):
    def __init__(self, destination: Parameter, inputs: deque[int]):
        super().__init__(2)
        self.inputs = inputs
        self.destination = destination

    def _run(self, registers: list[int]):
        if not self.inputs:
            return ExecutionState.PAUSED, 0
        registers[self.destination.get_destination()] = self.inputs.popleft()


class WriteOut(RunningOperation):
    def __init__(self, param: Parameter, outputs: deque[int]):
        super().__init__(2)
        self.outputs = outputs
        self.param = param

    def _run(self, registers: list[int]):
        self.outputs.append(self.param.get_value(registers))


class AdjustRelativeBase(RunningOperation):
    def __init__(self, param: Parameter, relative_base: RelativeBase):
        super().__init__(2)
        self.param = param
        self.relative_base = relative_base

    def _run(self, registers: list[int]):
        self.relative_base.adjust(self.param.get_value(registers))
