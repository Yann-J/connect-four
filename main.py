# -*- coding: utf-8 -*-
from rich import print

import sys

# Constants
BOARD_SIZE = (7, 6)  # (width, height)
WIN_SEQUENCE_LENGTH = 4
PLAYERS = (
    {"name": "Player 1", "colour": "yellow", "symbol": "X"},
    {"name": "Player 2", "colour": "red", "symbol": "O"},
    # {"name": "Charlie", "colour": "green", "symbol": "I"},
)


# Read constants from cmd line arguments
sys.argv = sys.argv[1:]
if len(sys.argv) >= 2:
    BOARD_SIZE = (int(sys.argv[0]), int(sys.argv[1]))
if len(sys.argv) == 3:
    WIN_SEQUENCE_LENGTH = int(sys.argv[2])


def print_board(game):
    board = game["board"]

    for y in range(game["height"] - 1, -1, -1):
        for x in range(game["width"]):
            if y < len(board[x]):
                player_details = PLAYERS[board[x][y]]
                print(
                    f"[{player_details['colour']}][{player_details['symbol']}]",
                    end="",
                )
            else:
                print("[gray][ ]", end="")
        print()

    for x in range(game["width"]):
        style = "black on red" if len(board[x]) == game["height"] else "blue"
        print(f"[{style}]{x+1:^3}[/]", end="")
    print()


def play_turn(game, column):
    board = game["board"]
    current_player = game["current_player"]

    if 0 <= column < len(board) and len(board[column]) < game["height"]:
        # Add to board
        board[column].append(current_player)
        # Next player
        game["current_player"] = (current_player + 1) % len(PLAYERS)
        return True
    else:
        return False


def all_equal(lst):
    return len(set(lst)) == 1


def check_winner(game):
    board = game["board"]

    # Check vertical
    for x in range(game["width"]):
        for y in range(game["height"] - (WIN_SEQUENCE_LENGTH - 1)):
            if len(board[x]) > y + (WIN_SEQUENCE_LENGTH - 1) and all_equal(
                board[x][y : y + WIN_SEQUENCE_LENGTH]
            ):
                return board[x][y]

    # Check horizontal
    for y in range(game["height"]):
        for x in range(game["width"] - (WIN_SEQUENCE_LENGTH - 1)):
            if all(
                [len(board[x + i]) > y for i in range(WIN_SEQUENCE_LENGTH)]
            ) and all_equal([board[x + i][y] for i in range(WIN_SEQUENCE_LENGTH)]):
                return board[x][y]

    # Check diagonal up
    for x in range(game["width"] - (WIN_SEQUENCE_LENGTH - 1)):
        for y in range(game["height"] - (WIN_SEQUENCE_LENGTH - 1)):
            if all(
                [len(board[x + i]) > y + i for i in range(WIN_SEQUENCE_LENGTH)]
            ) and all_equal([board[x + i][y + i] for i in range(WIN_SEQUENCE_LENGTH)]):
                return board[x][y]

    # Check diagonal down
    for x in range(game["width"] - (WIN_SEQUENCE_LENGTH - 1)):
        for y in range((WIN_SEQUENCE_LENGTH - 1), game["height"]):
            if all(
                [len(board[x + i]) > y - i for i in range(WIN_SEQUENCE_LENGTH)]
            ) and all_equal([board[x + i][y - i] for i in range(WIN_SEQUENCE_LENGTH)]):
                return board[x][y]

    # Check draw (board full)
    if all([len(board[x]) == game["height"] for x in range(game["width"])]):
        return -1

    return None


if __name__ == "__main__":
    print(f"Welcome to Connect-{WIN_SEQUENCE_LENGTH}!")

    # Board is a list of columns, each column is a stack of colours played
    game_state = {
        "width": BOARD_SIZE[0],
        "height": BOARD_SIZE[1],
        "board": [[] for _ in range(BOARD_SIZE[0])],
        "current_player": 0,
    }

    print_board(game_state)

    while True:
        player = PLAYERS[game_state["current_player"]]
        board = game_state["board"]

        print(f"{player['name']}'s turn: [{player['colour']}]{player['symbol']}")
        valid_move = False
        while not valid_move:
            try:
                column = int(input("Your play: "))
                valid_move = play_turn(game_state, column - 1)
            except ValueError:
                pass
            if not valid_move:
                print(
                    f"❌ Invalid move! Please enter a number between 1 and {game_state['width']} for a column that isn't full."
                )
        print_board(game_state)

        winner = check_winner(game_state)
        if winner is not None:
            if winner == -1:
                print("It's a draw! 🤝")
            else:
                print(f"{PLAYERS[winner]['name']} wins! 🏆")
            sys.exit()
