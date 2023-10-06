def part1(input):
    answers = parse(input)
    answer_count = 0

    for a in answers:
        all_answered = []
        # have the answers the members gave individually and check for each answer given in general
        # if that answer was given by all members
        a = a.split("\n")
        for letter in set("".join(a)):
            if all(letter in answer for answer in a):
                all_answered.append(letter)
            # since a set of all the answers is iterated, it contains all of the answers given 1 time
            answer_count += 1

    return answer_count


def part2(input):
    answers = parse(input)
    answer_count = 0

    for a in answers:
        all_answered = []
        # have the answers the members gave individually and check for each answer given in general
        # if that answer was given by all members
        a = a.split("\n")
        for letter in set("".join(a)):
            if all(letter in answer for answer in a):
                all_answered.append(letter)
            # since a set of all the answers is iterated, it contains all of the answers given 1 time
        answer_count += len(all_answered)

    return answer_count


def parse(input: str):
    return input.split("\n\n")
