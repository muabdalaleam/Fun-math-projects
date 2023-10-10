"""
Tic Tac Toe Player
"""

import pyfiglet
import os
import pyfiglet
import random
import time
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state() -> list[list]:
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def board_to_matrix(board: list[list], return_all=False):
    """
    This function converts tictactoe board into a
    tuple of rows & cols instead of nested lists
    """

    # Creating empty placeholders for the returns
    columns = {0: [], 1: [], 2: []}
    rows = {0: [], 1: [], 2: []}
    diagonals = {0: [], 1: []}

    data_1D = []

    # Creating rows and columns using the dicts
    for row, row_idx in zip(board, rows.keys()):
        for row_unit, col_idx in zip(row, columns.keys()):
            rows[row_idx].append(row_unit)
            columns[col_idx].append(row_unit)

    # Creating diagonal dict for from the right & the left
    for i, j in zip([0, 1, 2], [-1, -2, 0]):
        diagonals[0].append(rows[i][i])
        diagonals[1].append(rows[i][j])

    # Create a list that will contain all of the data
    for col in columns.values():
        for unit in col:
            data_1D.append(unit)

    if return_all:
        return data_1D
    else:
        return (rows, columns, diagonals)


def player(board: list[list]) -> str:
    turn = 0  # this value will be odd for X turn and even for O
    plays = board_to_matrix(board, return_all=True)

    if plays.count(O) > plays.count(X):
        turn += 2
    elif plays.count(X) > plays.count(O):
        turn += 1

    if turn % 2 == 0:
        return X
    else:
        return O


def actions(board: list[list]) -> set[tuple]:
    possible_actions = []

    for row_idx in board_to_matrix(board)[0].keys():
        for col_idx in board_to_matrix(board)[1].keys():
            if board[row_idx][col_idx] == EMPTY:
                possible_actions.append(tuple((row_idx, col_idx)))

    return set(possible_actions)


def result(board: list[list], action: tuple) -> list[list]:
    board = copy.deepcopy(board)

    if action not in actions(board):
        raise Exception("Weird")
    else:
        row, col = action
        board[row][col] = player(board)

    return board


def winner(board: list[list]) -> str:
    rows = board_to_matrix(board)[0]
    cols = board_to_matrix(board)[1]
    diags = board_to_matrix(board)[2]

    for row in rows.values():
        for col in cols.values():
            if all(unit == row[0] for unit in row) and row[0] != EMPTY:
                return row[0]
            elif all(unit == col[0] for unit in col) and col[0] != EMPTY:
                return col[0]

    for diag in diags.values():
        if all(unit == diag[0] for unit in diag) and diag[0] != EMPTY:
            return diag[0]


def terminal(board: list[list]) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    # the game is over when X or O is the winner
    if winner(board) in (X, O):
        return True

    # or if the board is full (i.e., there are no EMPTY anymore)
    if EMPTY not in board_to_matrix(board, return_all=True):
        return True

    return False


def utility(board: list[list]) -> int:
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0


def min_value(board: list[list]) -> tuple[int, tuple]:
    if terminal(board):
        return (utility(board), None)

    best_value = float("inf")
    best_move = None

    for action in actions(board):
        move_value = max_value(result(board, action))[0]

        if move_value < best_value:
            best_move = action
            best_value = move_value

    return (best_value, best_move)


def max_value(board: list[list]) -> tuple[int, tuple]:
    if terminal(board):
        return (utility(board), None)

    best_move = None
    best_value = float("-inf")

    for action in actions(board):
        move_value = min_value(result(board, action))[0]

        if move_value > best_value:
            best_move = action
            best_value = move_value

    return (best_value, best_move)


def minimax(board: list[list]) -> tuple[int, int]:
    """
    @params: This function takes the state of the game
    @return: The best move in a tuple
    """
    current_player = player(board)
    max_player = X
    min_player = O

    if current_player == min_player:
        return min_value(board)[1]
    elif current_player == max_player:
        return max_value(board)[1]


X = "X"
O = "O"
EMPTY = " "


def draw_board(board: list[list[str]]) -> None:
    board_copy = copy.deepcopy(board)
    emp_cell_idx = 0

    for inner_list in board_copy:
        for i in range(len(inner_list)):
            if inner_list[i] is None:
                emp_cell_idx += 1
                inner_list[i] = f"{emp_cell_idx}"

    printable_board = []
    for row in board_copy:
        printable_board.append(" | ".join(row))
        printable_board.append("-" * 9)

    print("\n".join(printable_board))


def main() -> None:

    def get_user_move() -> tuple[int, int]:
        while True:
            row = input("Enter row from the board with one based indexing: ")
            col = input("Enter column from the " + \
                        "board with one based indexing: ")

            try:
                row = int(row) - 1
                col = int(col) - 1
            except ValueError:
                print("Please input the rows and columns as integers.\n\n")
                continue

            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Invalid row or column.")
                continue

            if board[row][col] != EMPTY:
                print("That square is already taken.")
                continue

            return row, col

    # This escape sequence make the text bold. : "\033[1;37m"
    # src: https://blog.finxter.com/how-to-print-bold-text-in-python/

    rules = "Game rules are so simple if you" + \
            "lose from the AI you'll get 0 score\n" + \
            "and if you got a draw you will get +1" + \
            "score but you can't win because\n" + \
            "MinMax algorithm never lose."


    welcome_messages = [
        "Welcome to Tic Tac Toe" + \
        "AI! Where you 'll never win!!",
        "Get ready for an " + \
        "exciting game of Tic Tac Toe!",
        "Prepare to challenge" + \
        " the AI in Tic Tac Toe!",
        "Let's play Tic Tac Toe "+ \
        " against the AI!",
    ]

    streak_score = 0
    title = "\033[1;37m" + pyfiglet.figlet_format(
    "Tic Tac Toe AI_", font="banner3-D", width=90
    ) + "\033[0m"

    welcome_message = "\033[1;37m" + random.choice(welcome_messages) + "\033[0m"

    print(title)
    print(welcome_message + "\n")
    print(rules + "\n")

    time.sleep(0.5)

    board = initial_state()
    user = None
    ai_turn = False

    while True:
        while user not in (X, O):
            user = input("Choose a player to play with"+ \
                        "from X, O (X starts first): ").title()

            if user not in (X, O):
                print("Please input a valid player from X, O")
                continue
            else:
                user = eval(user)

        time.sleep(0.3)
        print("\n\nThe current board:")
        draw_board(board)

        game_over = terminal(board)
        player_ = player(board)

        if game_over:
            winner_ = winner(board)

            if winner_ is None:
                streak_score += 1
                print("\n\nGame Over: Tie.")

            elif winner_ is player_:
                streak_score += float('inf')
                print("YOU ARE HACKER HOW DID YOU DO THIS ?!!!!")
                print(f"\n\nYou as {player_} won the game WOW!.")

            else:
                print(f"\n\nComputer wins as {winner_}.")
                pass

        elif user == player_:
            print(f"\n\nPlay as {user}")

        else:
            print(f"\n\nComputer thinking...")

        if user != player_ and not game_over:
            if ai_turn:
                time.sleep(0.3)
                move = minimax(board)
                board = result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        if user == player_ and not game_over:
            board = result(board, get_user_move())

        if game_over:
            print(f"Your current streak score is: {streak_score}")
            play_again = input("Would you like to play again (y, n): ")

            if play_again.lower() == "y":

                os.system('cls' if os.name == 'nt' else 'clear')
                main()

            else:
                print(
                    "\033[1;37m"
                    + "Thanks for playing.\n"
                    + "My website: https://muhammed-abdelaleam.github.io/me/"
                    + "\033[0m"
                )
                break


if __name__ == "__main__":
    main()