import flask
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False  # Be forgiving with trailing slashes in URL

SAMPLE_GAME = {
    "game_id": 1,
    "players_turn": "X",
    "status": "in progress",  # may also be "x wins", "o wins", or "tie"
    "board": [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
}

SAMPLE_MOVE = {
    "players_turn": "X",
    "x_position": 1,
    "y_position": 1
}

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
        return "Game not found", 404

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
        return "Game not found", 404

    # Check if game is over
    if not game["status"] == "in progress":
        return "This game is already over", 400

    move = flask.request.get_json()  # Converts input data to JSON
    player = move["players_turn"]
    x = move["x_position"]
    y = move["y_position"]

    # Check if it's your turn
    if not game["players_turn"] == player:
        return "Its not your turn\n", 400

    # Validate that this move is valid
    if x > 2 or y > 2:
        return "Out of bounds\n", 400

    if not game["board"][x][y] == " ":
        return "Invalid move\n", 400

    # Update the game's board
    game["board"][x][y] = player
    game["players_turn"] = "X" if (player == "Y") else "Y"
    GAMES[game_id] = game

     # TODO: check if game is over (tie/win)

    return flask.jsonify(game), 200
