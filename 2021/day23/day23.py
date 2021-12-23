import heapq


class CustomPriorityQueue:
    def __init__(self):
        self.queue = []
        self.costs = dict()

    def empty(self) -> bool:
        return len(self.queue) == 0

    def put(self, entry: tuple):
        heapq.heappush(self.queue, entry)
        self.costs["".join(entry[1])] = entry[0]

    def get(self) -> tuple:
        return heapq.heappop(self.queue)

    def cost_if_contains(self, state: list) -> int:
        return self.costs.get("".join(state), None)


def solve(initial_state: list, end: list) -> int:
    global energy_cost, target

    states = CustomPriorityQueue()
    states.put((0, initial_state))

    while not states.empty():
        cost, current = states.get()
        if current == end:
            return cost

        for c, s in get_legal_states(cost, current):
            saved_cost = states.cost_if_contains(s)
            if saved_cost is None or c < saved_cost:
                states.put((c, s))


def get_legal_states(cost: int, state: list) -> list:
    global energy_cost, target

    legal_states = []

    # letters on the hallway: try to move into the correct room
    for i in [0, 1, 3, 5, 7, 9, 10]:
        if state[i] != ".":
            letter = state[i]

            # try to go into the room
            if can_reach(i, target[letter], state):
                room = state[target[letter]][::-1]

                can_enter = True
                for lett in room:
                    if lett not in [letter, "."]:
                        can_enter = False
                        break
                if not can_enter:
                    continue

                free_index = room.index(".")
                move_cost = (abs(i - target[letter]) + free_index + 1) * energy_cost[letter]
                new_state = state[:]
                new_state[i] = "."
                new_room = room[:free_index] + letter + room[free_index + 1:]

                new_state[target[letter]] = new_room[::-1]

                legal_states.append((cost + move_cost, new_state))

    # letters in the room: try to move onto the hallway
    for i in [2, 4, 6, 8]:
        room = state[i]
        need_move = False
        for lett in room:
            if lett == ".":
                continue
            if target[lett] != i:
                need_move = True

        if not need_move:
            continue

        letter = None
        for lett in room:
            if lett == ".":
                continue
            else:
                letter = lett
                break

        letter_index = room.index(letter)

        for j in [0, 1, 3, 5, 7, 9, 10]:
            if can_reach(i, j, state):
                move_cost = (abs(i - j) + letter_index + 1) * energy_cost[letter]
                new_state = state[:]
                new_room = room[:letter_index] + "." + room[letter_index + 1:]
                new_state[i] = new_room
                new_state[j] = letter
                legal_states.append((cost + move_cost, new_state))

    return legal_states


def can_reach(pos1: int, pos2: int, state: list) -> bool:
    global target

    a = min(pos1, pos2)
    b = max(pos1, pos2)

    for i in range(a, b + 1):
        if i == pos1:
            continue

        if len(state[i]) > 1:
            continue

        if state[i] != ".":
            return False

    return True


if __name__ == "__main__":
    energy_cost = {"A": 1, "B": 10, "C": 100, "D": 1000}
    target = {"A": 2, "B": 4, "C": 6, "D": 8}

    input1 = [".", ".", "AC", ".", "DD", ".", "AB", ".", "CB", ".", "."]
    end1 = [".", ".", "AA", ".", "BB", ".", "CC", ".", "DD", ".", "."]

    input2 = [".", ".", "ADDC", ".", "DCBD", ".", "ABAB", ".", "CACB", ".", "."]
    end2 = [".", ".", "AAAA", ".", "BBBB", ".", "CCCC", ".", "DDDD", ".", "."]

    print(f"Part 1: The minimum amount of energy is {solve(input1, end1)}.")

    print(f"Part 2: The minimum amount of energy is {solve(input2, end2)}.")
