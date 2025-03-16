board_size = 50
# 2 dimensional array of tiles. False means the white side is up, True means the white side is up


def part1(input):
    instructions = [instructions for instructions in input.splitlines()]
    board = prepare_board(instructions)

    return sum(row.count(True) for row in board)


def part2(input):
    instructions = [instructions for instructions in input.splitlines()]
    board = prepare_board(instructions)

    black_tiles = get_black_tiles(board)
    black_tiles = simulate(black_tiles)

    return len(black_tiles)


def prepare_board(instructions):
    board = [[False for _ in range(board_size)] for _ in range(board_size)]
    fill_board(board, instructions)

    return board


def fill_board(board, instructions):
    for instruction in instructions:
        # q and r as offsets in a grid. q are the columns, r are the rows
        q = r = board_size // 2
        i = 0
        while i < len(instruction):
            if instruction[i] == "e":
                q += 1
            elif instruction[i] == "w":
                q -= 1
            elif instruction[i] == "n":
                i += 1
                if instruction[i] == "e":
                    q += 1
                    r -= 1
                else:
                    r -= 1
            elif instruction[i] == "s":
                i += 1
                if instruction[i] == "w":
                    q -= 1
                    r += 1
                else:
                    r += 1
            i += 1

        board[r][q] = not board[r][q]


def get_neighbours(tile):
    neighbours = set()
    for dr, dq in [[1, 0], [1, -1], [0, -1], [-1, 0], [0, 1], [-1, 1]]:
        neighbours.add((tile[0] + dr, tile[1] + dq))
    return neighbours


def count_black_neighbours(tile, black_tiles):
    count = 0
    for neighbour in get_neighbours(tile):
        if neighbour in black_tiles:
            count += 1
    return count


def get_black_tiles(board):
    foo = set()
    for r in range(board_size):
        for q in range(board_size):
            if board[r][q]:
                foo.add((r, q))
    return foo


def simulate(black_tiles):
    for _ in range(100):
        tiles = set()
        black_copy = black_tiles.copy()

        # the black tiles and all its neighbours are subjected to change
        for tile in black_tiles:
            tiles.add(tile)
            for neighbour in get_neighbours(tile):
                tiles.add(neighbour)

        while len(tiles) > 0:
            tile = tiles.pop()

            # look at the neighbours of the tile and count the black tiles
            black_neighbours = count_black_neighbours(tile, black_tiles)

            # flip a black tile to white
            if tile in black_tiles and (black_neighbours == 0 or black_neighbours > 2):
                black_copy.remove(tile)
            # flip a white tile to black
            elif tile not in black_tiles and black_neighbours == 2:
                black_copy.add(tile)

        black_tiles = black_copy

    return black_tiles
