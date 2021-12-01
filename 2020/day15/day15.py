starting_numbers = [2, 0, 1, 7, 4, 14, 18]

memory = {starting_numbers[i]: i + 1 for i in range(len(starting_numbers) - 1)}

most_recently = starting_numbers[-1]
current_count = len(starting_numbers)

while True:
    if current_count == 30000000:
        print(most_recently)
        break

    if most_recently not in memory.keys():
        memory[most_recently] = current_count
        most_recently = 0
    else:
        z = current_count - memory[most_recently]
        memory[most_recently] = current_count
        most_recently = z

    current_count += 1
