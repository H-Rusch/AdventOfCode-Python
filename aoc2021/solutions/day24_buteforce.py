from functools import cache


@cache
def execute_batch(z_in: int, w_in: int, index: int) -> int:
    global AS, BS, CS

    z = z_in

    x = int((z % 26) + BS[index] != w_in)
    z //= AS[index]
    z *= 25 * x + 1
    z += (w_in + CS[index]) * x

    return z


def solve(index: int, z: int, search_max: bool):
    global state_dict

    key = (index, z)

    if key in state_dict:
        return state_dict[key]

    found = None

    # search through descending numbers to get the maximum number
    # and through ascending numbers to get the minimum number
    numbers = [9, 8, 7, 6, 5, 4, 3, 2, 1] if search_max else [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for w in numbers:
        new_z = execute_batch(z, w, index)

        if index == 13:
            if new_z == 0:
                found = str(w)
                break
            else:
                found = None

        else:
            found = solve(index + 1, new_z, search_max)
            if found is not None:
                found = str(w) + found
                break

    state_dict[key] = found
    return found


if __name__ == "__main__":
    state_dict = dict()
    AS = [1, 1, 1, 1, 26, 1, 1, 26, 1, 26, 26, 26, 26, 26]
    BS = [14, 13, 15, 13, -2, 10, 13, -15, 11, -9, -9, -7, -4, -6]
    CS = [0, 12, 14, 0, 3, 15, 11, 12, 1, 12, 3, 10, 14, 12]

    print(f"Part 1: The biggest accepted model number is {solve(0, 0, True)}.")

    state_dict.clear()

    print(f"Part 2: The smallest accepted model number is {solve(0, 0, False)}.")
