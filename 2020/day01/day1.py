# read input
file = open("input_day1.txt", "r")
input = [int(i) for i in file.read().splitlines()]
file.close()

# First half of puzzle
for i in range(len(input) - 1):
    for j in range(i + 1, len(input)):
        summ = input[i] + input[j]
        if summ == 2020:
            print(input[i] * input[j])
            break

# Second half of puzzle
for i in range(len(input) - 1):
    for j in range(i + 1, len(input)):
        for k in range(j + 1, len(input)):
            summ = input[i] + input[j] + input[k]
            if summ == 2020:
                print(input[i] * input[j] * input[k])
                break
