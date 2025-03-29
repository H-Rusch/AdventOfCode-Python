from enum import Enum


class ExecutionState(Enum):
    INITIAL = 0
    RUNNING = 1
    PAUSED = 2
    HALTED = 3
