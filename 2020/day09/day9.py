
def check_sum_in_last_25(to_search: int, numbers: list):
    # iterate over list of numbers after the preamble of 25
    for i in range(len(numbers)):
        for j in range(i, len(numbers)):
            if i != j:
                if numbers[i] + numbers[j] == to_search:
                    return True
    return False



# read in numbers
file = open("input.txt", "r")
numbers = [int(n) for n in file.read().split("\n")]
file.close()

# part 1
invalid_number = -1
# find first number which isn't the sum of 2 numbers in the 25 numbers before it
for k in range(25, len(numbers)):
    checking_for = numbers[k]
    # number not found as a sum of 2 numbers in the last 25 numbers
    if not check_sum_in_last_25(checking_for, numbers[k - 25:k]):
        print(str(checking_for) + " is the first without the property.")
        invalid_number = checking_for
        break

# part 2
# iterate over the list and sum continuous elements to get the invalid number.
# If the value of the invalid number is met print the minimum and the maximum of the elements
for i in range(len(numbers) - 1):
    sum_to_invalid = numbers[i]
    j = i
    while sum_to_invalid < invalid_number:
        j += 1
        sum_to_invalid += numbers[j]
        if sum_to_invalid > invalid_number:
            break
        elif sum_to_invalid == invalid_number:
            subset = numbers[i:j]
            print(str(min(subset) + max(subset)) + " is the encryption weakness.")
            quit()


