def part_1(number_list):
    times_increasing = 0

    for n, n_1 in zip(number_list[0::], number_list[1::]):
        if n < n_1:
            times_increasing += 1

    print(f"Part 1: The numbers increase {times_increasing} times.")


def part_2(number_list, sliding_size=3):
    times_increasing = 0
    last_sliding_sum = sum(number_list[:sliding_size])

    for i in range(1, len(number_list) - sliding_size + 1):
        sliding = number_list[i:i + sliding_size]
        sliding_sum = sum(sliding)

        if last_sliding_sum < sliding_sum:
            times_increasing += 1

        last_sliding_sum = sliding_sum

    print(f"Part 2: The value of the sums increases {times_increasing} times.")


if __name__ == "__main__":
    with open("input.txt", 'r', encoding='utf-8') as file:
        numbers = [int(s) for s in file.read().splitlines()]

        part_1(numbers)

        part_2(numbers)
