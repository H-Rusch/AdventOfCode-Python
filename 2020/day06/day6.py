# read in answers
file = open("input.txt", "r")
answers = file.read().split("\n\n")
file.close()

answer_count1 = 0
answer_count2 = 0
# go through all groups
for a in answers:
    all_answered = []
    # have the answers the members gave individually and check for each answer given in general
    # if that answer was given by all members
    a = a.split("\n")
    for letter in set("".join(a)):
        if all(letter in answer for answer in a):
            all_answered.append(letter)
        # since a set of all the answers is iterated, it contains all of the answers given 1 time
        answer_count1 += 1
    answer_count2 += len(all_answered)

print(answer_count1)
print(answer_count2)


