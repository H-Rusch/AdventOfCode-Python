class BingoBoard:
    def __init__(self, number_list: list):
        self.bingo_board = number_list
        self.marked = [[False for _ in range(len(self.bingo_board))] for _ in range(len(self.bingo_board))]

    def mark_number(self, number: str) -> bool:
        """
        Mark the drawn number on the bingo sheet if the number is present.
        """
        for i in range(len(self.bingo_board)):
            for j in range(len(self.bingo_board[i])):
                if self.bingo_board[i][j] == number:
                    self.marked[i][j] = True
                    return True

        return False

    def check_finished(self) -> bool:
        """
        Check whether the bingo board has all numbers marked in any column or row.
        """
        for i in range(len(self.marked)):
            if all(self.marked[i]) or all([self.marked[j][i] for j in range(len(self.marked))]):
                return True

        return False

    def sum_unmarked(self) -> int:
        sum_of_unmarked = 0

        for i in range(len(self.bingo_board)):
            for j in range(len(self.bingo_board[i])):
                if not self.marked[i][j]:
                    sum_of_unmarked += int(self.bingo_board[i][j])

        return sum_of_unmarked

    def print(self):
        print("Bingo Board:")
        for line in self.bingo_board:
            print("\t".join(line))

        print("Marked:")
        for line in self.marked:
            print("\t".join([str(b) for b in line]))


def part_1(number_list: list, board_list: list):
    bingo_boards = [BingoBoard(board) for board in board_list]

    winner, winning_number = get_first_winning_board(number_list, bingo_boards)
    # winner.print()
    final_score = winner.sum_unmarked() * winning_number

    print(f"Part 1: The final score for the first winning bingo board is {final_score}.")


def part_2(number_list: list, board_list: list):
    bingo_boards = [BingoBoard(board) for board in board_list]

    winner, winning_number = get_last_winning_board(number_list, bingo_boards)
    # winner.print()
    final_score = winner.sum_unmarked() * winning_number

    print(f"Part 2: The final score for the last winning bingo board is {final_score}.")


def get_first_winning_board(number_list: list, board_list: list) -> (BingoBoard, int):
    for number in number_list:
        for board in board_list:
            if board.mark_number(number) and board.check_finished():
                return board, int(number)


def get_last_winning_board(number_list: list, board_list: list) -> (BingoBoard, int):
    for number in number_list:
        for board in board_list[:]:
            if board.mark_number(number) and board.check_finished():
                if len(board_list) > 1:
                    board_list.remove(board)
                else:
                    return board, int(number)


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        lines = file.read().split("\n\n")

        draw_input = lines[0].split(",")
        board_input = [line.split("\n") for line in lines[1:]]
        board_input = [[line.replace("  ", " ").split() for line in board_input[i]] for i in range(len(board_input))]

        part_1(draw_input, board_input)

        part_2(draw_input, board_input)
