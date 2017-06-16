import flask
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False  # Be forgiving with trailing slashes in URL

GAMES = {}
NUMGAMES = 0

@app.route("/games", methods=['POST'])
def create_game():
    r"""
    Creates an initialized game of tic tac toe with a unique game_id.

    :return: a newly initialized game status with status code of 201
    """

    # Create and persist a unique game
    global NUMGAMES, GAMES
    NUMGAMES +=1
    game_id = NUMGAMES
    game = {
        "game_id": game_id,
        "players_turn": "X",
        "status": "in progress",
        "board": [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
        ]
    }

    GAMES[game_id] = game
    return flask.jsonify(game), 201


@app.route("/games/<int:game_id>", methods=['GET'])
def get_game_status(game_id):
    r"""
    Fetches the current status of the game of tic tac toe.

    :param game_id: unique identifier of tic-tac-toe
    :return: if game exists, return current game status.
                otherwise, return status code 404
    """

    # Look this game up from some place that holds all of the games
    game = GAMES.get(game_id)
    if not game:
        # This is an unknown game
        return "Game not found\n", 404

    game = GAMES[game_id]
    return flask.jsonify(game)


@app.route("/games/<int:game_id>", methods=['PUT'])
def make_move(game_id):
    r"""
    Makes a move on behalf of a player on the provided game_id.

    :param game_id:
    :return: if game ID exists and the move is valid, return game status after the move is played.
                if the game is not found, return 404 status code
                if the move is a bad request, return 400 status code
    """

    # Look this game up from some place that holds all of the games
    global NUMGAMES, GAMES
    # Check if game exists
    game = GAMES.get(game_id)
    if not game:
        return "Game not found\n", 404

    # Check if game is over
    if not game["status"] == "in progress":
        return "This game is already over\n", 400

    move = flask.request.get_json()  # Converts input data to JSON
    player = move["players_turn"]
    # input (1,0) = row 0, column 1 -> i = 0, j = 1
    i = move["y_position"]
    j = move["x_position"]

    # Check if it's your turn
    if not game["players_turn"] == player:
        return "Its not your turn\n", 400

    # Validate that this move is valid
    if i > 2 or j > 2:
        return "Out of bounds\n", 400

    if not game["board"][i][j] == " ":
        return "Invalid move\n", 400

    # Update the game's board
    game["board"][i][j] = player
    game["players_turn"] = "X" if (player == "O") else "O"

    # check if game is over 
    if checkWin(game["board"], player):
        game["status"] = player.lower() + " wins"
        GAMES[game_id] = game
        return flask.jsonify(game)

    if isFull(game["board"]):
        game["status"] = "tie"

    GAMES[game_id] = game
    return flask.jsonify(game)

def checkWin(board, player):
    # check columns and rows
    for i in range(0,3):
        if(board[i][0] == board[i][1] == board[i][2] == player) or \
        (board[0][i] == board[1][i] == board[2][i] == player):
            return True
    # check diagonals
    if (board[0][0] == board[1][1] == board[2][2] == player) or \
    (board[2][0] == board[1][1] == board[0][2] == player):
        return True
    return False

def isFull(board):
    for row in board:
        if " " in row:
            return False
    return True
