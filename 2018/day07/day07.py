import re
import string
from collections import defaultdict


class Step:
    def __init__(self, letter):
        self.letter = letter
        self.prereq = set()
        self.enables = set()

    def remove_prereq(self, step: "Step"):
        self.prereq.remove(step)

    def destroy(self):
        if len(self.prereq) == 0:
            for enabled in self.enables:
                enabled.remove_prereq(self)

    def __repr__(self):
        return "s(" + self.letter + ")"


class Worker:
    def __init__(self):
        self.end = -1
        self.current = None

    def set_work(self, step: Step, t: int):
        self.current = step
        self.end = t + get_time(step.letter)

    def __repr__(self):
        return "r(" + repr(self.current) + ", " + str(self.end) + ")"


class WorkerFactory:
    def __init__(self, size: int):
        self.workers = [Worker() for _ in range(size)]
        self.queued_steps = []
        self.t = 0
        self.letters = ""

    def queue_step(self, step: Step):
        self.queued_steps.append(step)
        self.queued_steps = sorted(self.queued_steps, key=lambda s: s.letter)

    def finish_steps(self):
        for worker in self.workers:
            if worker.end == self.t:
                worker.current.destroy()
                self.letters += worker.current.letter
                worker.current = None

    def distribute_work(self):
        free_workers = self.find_free_workers()

        for worker in free_workers:
            if len(self.queued_steps) == 0:
                break
            worker.set_work(self.queued_steps.pop(0), self.t)

    def find_free_workers(self) -> list:
        free_workers = []
        for worker in self.workers:
            if worker.end <= self.t:
                free_workers.append(worker)

        return free_workers


def part_1(steps: dict) -> str:
    letters = ""

    candidates = []
    while len(steps.items()) > 0:
        # find steps with no prerequisite and order the candidates alphabetically
        for letter in string.ascii_uppercase:
            if letter in steps and steps[letter] not in candidates and len(steps[letter].prereq) == 0:
                candidates.append(steps[letter])
        candidates = sorted(candidates, key=lambda c: c.letter)

        # get first candidate and remove it from all steps it enables. Remove the candidate from the steps collection
        candidate = candidates.pop(0)
        letters += candidate.letter
        candidate.destroy()
        del steps[candidate.letter]

    return letters


def part_2(steps: dict) -> int:
    factory = WorkerFactory(5)
    target = len(steps)

    while len(factory.letters) != target:
        factory.finish_steps()

        for letter in string.ascii_uppercase:
            if letter in steps and len(steps[letter].prereq) == 0:
                factory.queue_step(steps[letter])
                del steps[letter]

        factory.distribute_work()
        factory.t += 1

    return factory.t - 1


def get_time(letter: str) -> int:
    return string.ascii_uppercase.index(letter) + 1 + 60


def parse_input():
    with open("input.txt", "r") as file:
        steps = dict()

        for line in file.read().strip().splitlines():
            l1, l2 = re.search(r"Step (.) must be finished before step (.) can begin.", line).groups()
            step1, step2 = steps.get(l1, Step(l1)), steps.get(l2, Step(l2))
            step2.prereq.add(step1)
            step1.enables.add(step2)
            steps[l1] = step1
            steps[l2] = step2

        return steps


if __name__ == "__main__":
    print(f"Part 1: The instructions should be completed in the order {part_1(parse_input())}.")

    print(f"Part 2: It takes {part_2(parse_input())} seconds to complete all the steps.")
