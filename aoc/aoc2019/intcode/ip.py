class InstructionPointer:
    def __init__(self):
        self.value = 0
        self.just_jumped = 0

    def increment(self, amount: int):
        if self.just_jumped:
            self.just_jumped = False
            return
        self.value += amount

    def jump(self, value: int):
        self.just_jumped = True
        self.value = value
