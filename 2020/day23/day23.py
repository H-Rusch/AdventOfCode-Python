class LinkedList:
    def __init__(self, elements=None):
        self.start = None
        self.last = None  # last to append faster
        self.element_lookup = dict()  # dictionary to get the element for a value fast
        if elements is not None:
            self.start = LinkedListElement(elements.pop(0))
            current = self.start
            self.last = current
            self.element_lookup[current.value] = current
            for element in elements:
                current.next = LinkedListElement(element)
                current = current.next
                self.last = current
                self.element_lookup[current.value] = current

    def get_first(self):
        return self.start

    def get_last(self):
        return self.last

    def get_by_value(self, value):
        return self.element_lookup[value]

    def append(self, element):
        if self.start is None:
            self.start = element
        else:
            self.get_last().next = element

    def print(self, starting_element):
        current = starting_element
        string = ""

        while current is not None:
            string += str(current.value) + " "
            current = current.next

            # break creating the string after the starting value has been encountered because this is going to be used
            # as a cycling list
            if current is not None and current.value == starting_element.value:
                string += "repeating"
                break
        print(string)

    def print_solution(self):
        starting_element = self.get_by_value(1)
        current = starting_element.next
        values = []

        while current is not None:
            values.append(current.value)
            current = current.next

            # break creating the string after the starting value has been encountered because this is going to be used
            # as a cycling list
            if current is not None and current.value == starting_element.value:
                break

        print("".join(str(i) for i in values))


class LinkedListElement:
    def __init__(self, value):
        self.value = value
        self.next = None


def part1():
    cup_input = [int(i) for i in "418976235"]
    min_cup = min(cup_input)
    max_cup = max(cup_input)

    cups = LinkedList(cup_input)
    cups.get_last().next = cups.get_first()

    current = cups.start
    for _ in range(100):
        # remove the next 3 elements after current from the list
        pick_up_start = current.next
        current.next = current.next.next.next.next
        picked_up = [pick_up_start.value, pick_up_start.next.value, pick_up_start.next.next.value]

        # calculate destination
        destination = current.value
        while True:
            destination -= 1
            if destination < min_cup:
                destination = max_cup
            if destination not in picked_up:
                break

        # insert the 3 taken cups after the destination cup
        destination_cup = cups.get_by_value(destination)
        after_destination = destination_cup.next
        destination_cup.next = pick_up_start
        pick_up_start.next.next.next = after_destination

        current = current.next

    cups.print_solution()


def part2():
    cup_input = [int(i) for i in "418976235"]
    for i in range(10, 1000001):
        cup_input.append(i)

    min_cup = min(cup_input)
    max_cup = max(cup_input)

    cups = LinkedList(cup_input)
    cups.get_last().next = cups.get_first()

    current = cups.start
    for _ in range(10000000):
        # remove the next 3 elements after current from the list
        pick_up_start = current.next
        current.next = current.next.next.next.next
        picked_up = [pick_up_start.value, pick_up_start.next.value, pick_up_start.next.next.value]

        # calculate destination
        destination = current.value
        while True:
            destination -= 1
            if destination < min_cup:
                destination = max_cup
            if destination not in picked_up:
                break

        # insert the 3 taken cups after the destination cup
        destination_cup = cups.get_by_value(destination)
        after_destination = destination_cup.next
        destination_cup.next = pick_up_start
        pick_up_start.next.next.next = after_destination

        current = current.next

    ones_cup = cups.get_by_value(1)
    print(ones_cup.next.next.value * ones_cup.next.value)


part1()
part2()