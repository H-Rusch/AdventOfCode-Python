def part_1(diagnostics: list):
    common_bits = [most_common_bit_at_position(diagnostics, i) for i in range(len(diagnostics[0]))]

    gamma_rate = "".join([str(i) for i in common_bits])
    epsilon_rate = complement(gamma_rate)

    power_consumption = int(gamma_rate, 2) * int(epsilon_rate, 2)
    print(f"Part 1: The power consumption is {power_consumption}.")


def part_2(diagnostic_data: list):
    life_support_rating = calculate_oxygen_rating(diagnostic_data) * calculate_co2_rating(diagnostic_data)
    print(f"Part 2: The life support rating is {life_support_rating}.")


def complement(binary_string):
    complement_string = "".join(["1" if binary_string[i] == "0" else "0" for i in range(len(binary_string))])
    return complement_string


def calculate_oxygen_rating(diagnostic_data: list) -> int:
    oxygen_list = diagnostic_data.copy()

    for i in range(len(diagnostic_data[0])):
        if len(oxygen_list) == 1:
            break
        bit_value = most_common_bit_at_position(oxygen_list, i)
        oxygen_list = list(filter(lambda bin_number: bin_number[i] == str(bit_value), oxygen_list))

    return int(oxygen_list[0], 2)


def calculate_co2_rating(diagnostic_data: list) -> int:
    co2_list = diagnostic_data.copy()

    for i in range(len(diagnostic_data[0])):
        if len(co2_list) == 1:
            break
        bit_value = least_common_bit_at_position(co2_list, i)
        co2_list = list(filter(lambda bin_number: bin_number[i] == str(bit_value), co2_list))

    return int(co2_list[0], 2)


def most_common_bit_at_position(diagnostic_data: list, position: int) -> int:
    number_of_ones = [diagnostic_data[i][position] for i in range(len(diagnostic_data))].count("1")

    if number_of_ones > len(diagnostic_data) / 2:
        return 1
    if number_of_ones < len(diagnostic_data) / 2:
        return 0

    # equal amounts -> return 1, so the most common bit can be kept for oxygen
    # and the least common bit can be kept by keeping the flipped result for co2
    return 1


def least_common_bit_at_position(diagnostic_data: list, position: int) -> int:
    return (most_common_bit_at_position(diagnostic_data, position) + 1) % 2


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        lines = [s for s in file.read().splitlines()]

        part_1(lines)
        part_2(lines)
