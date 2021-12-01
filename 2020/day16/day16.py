import re


# horrible, but it works I guess..


def create_rule_dict(rules: str):
    # create a rule dictionary which knows the ranges for values for each different field
    range_regex = re.compile(r"(\d*)-(\d*) or (\d*)-(\d*)")
    rule_dict = dict()
    for rule in rules.split("\n"):
        match = range_regex.search(rule).groups()
        rule_dict[rule[:rule.find(":")]] = [int(i) for i in match]

    return rule_dict


def check_valid(number: int, rule_dict: dict):
    # check if the value is in a range specified by the rules
    for rule in rule_dict.values():
        if rule[0] <= number <= rule[1] or rule[2] <= number <= rule[3]:
            return True
    return False


def part1(rule_dict: dict, tickets: str):
    tickets = tickets.split("\n")[1:]
    # valid tickets for part 2
    valid_tickets = tickets[:]

    # find invalid tickets with values which are in none of the ranges of any field
    invalid_rate = 0
    for ticket in tickets:
        for value in ticket.split(","):
            if not check_valid(int(value), rule_dict):
                invalid_rate += int(value)
                valid_tickets.remove(ticket)
                break

    print(invalid_rate)
    return valid_tickets


def filter(assignment: list, index: int, rule: str):
    for i in range(len(assignment)):
        if i != index and rule in assignment[i]:
            assignment[i].remove(rule)
            if len(assignment[i]) == 1:
                filter(assignment, i, assignment[i][0])


def part2(my_ticket: str, tickets: list, rule_dict: dict):
    assignment = [list(rule_dict.keys()) for _ in range(len(tickets[0].split(",")))]

    # iterate over each ticket
    for i in range(len(tickets)):
        ticket = [int(num) for num in tickets[i].split(",")]
        # iterate over each value in the ticket
        for j in range(len(ticket)):
            value = ticket[j]
            # check each rule by getting its interval and testing if the value is in that interval. If not the rule is
            # not in that column and will be removed from the list of rules for that column
            for rule in list(rule_dict.keys()):
                interval = rule_dict[rule]
                if not (interval[0] <= value <= interval[1] or interval[2] <= value <= interval[3]):
                    assignment[j].remove(rule)
                    # if only 1 entry is left for one column, go through the other columns and remove the assigned entry
                    if len(assignment[j]) == 1:
                        filter(assignment, j, assignment[j][0])

    multiply_departure = 1
    my_ticket = [int(n) for n in my_ticket.split(",")]
    for i in range(len(assignment)):
        if assignment[i][0].startswith("departure "):
            multiply_departure *= my_ticket[i]
    print(multiply_departure)


# read in tickets
with open("input.txt", "r") as file:
    ticket_info = [direct for direct in file.read().split("\n\n")]

rules_dict = create_rule_dict(ticket_info[0])

valid = part1(rules_dict, ticket_info[2])

part2(ticket_info[1].split("\n")[1], valid, rules_dict)
