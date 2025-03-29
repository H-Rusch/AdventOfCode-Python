from abc import ABC, abstractmethod


class Parameter(ABC):
    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        return False

    @abstractmethod
    def get_destination(self) -> int:
        pass

    @abstractmethod
    def get_value(self, registers: list[int]) -> int:
        pass


class Position(Parameter):
    def get_value(self, registers: list[int]) -> int:
        return registers[self.value]

    def get_destination(self) -> int:
        return self.value


class Immediate(Parameter):
    def get_value(self, _: list[int]) -> int:
        return self.value

    def get_destination(self) -> int:
        raise Exception("Immediate parameter can not be used for destination")


class Relative(Parameter):
    def __init__(self, value: int, base: int):
        super().__init__(value)
        self.base = base
        self.position = Position(value + base)

    def get_value(self, registers: list[int]) -> int:
        return self.position.get_value(registers)

    def get_destination(self) -> int:
        return self.position.get_destination()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value and self.base == other.base
        return False
