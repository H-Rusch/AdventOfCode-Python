def part1(input):
    boarding_passes = input.splitlines()
    seat_ids, _ = get_seats(boarding_passes)

    return max(seat_ids)


def part2(input):
    boarding_passes = input.splitlines()
    _, seats = get_seats(boarding_passes)

    # remove all None values from the list. These don't have a boarding pass
    for i in range(seats.count(None)):
        seats.remove(None)

    # go through the list to check for the seat_id "jumping" 2 spaces instead of 1. This is the missing seat
    for i in range(1, len(seats)):
        if seats[i] - seats[i - 1] != 1:
            return seats[i] - 1


def get_seats(boarding_passes: list) -> tuple:
    seat_ids = []
    seats = [None for _ in range(8 * 128)]

    for s in boarding_passes:
        # convert row code to binary number
        row = s[:7]
        row = row.replace("F", "0")
        row = row.replace("B", "1")
        row_num = int(row, 2)

        # convert seat code to binary number
        seat = s[7:]
        seat = seat.replace("L", "0")
        seat = seat.replace("R", "1")
        seat_num = int(seat, 2)

        # calculate seat id and add it to the list
        seat_id = row_num * 8 + seat_num
        seat_ids.append(seat_id)

        seats[row_num * 8 + seat_num] = seat_id

    return seat_ids, seats
