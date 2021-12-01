def transform(target_value: int):
    value = 1
    loop_size = 0
    while value != target_value:
        value *= 7
        value = value % 20201227
        loop_size += 1
    return loop_size


def calculate_encryption_key(loop_size: int, subject_number: int):
    value = 1
    for i in range(loop_size):
        value *= subject_number
        value = value % 20201227
    return value


door_public_key = 11349501
card_public_key = 5107328

card_loop_size = transform(card_public_key)

encryption_key = calculate_encryption_key(card_loop_size, door_public_key)

print(encryption_key)  # part 1
