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


@app.route("/games", methods=['POST'])
def create_game():
    r"""
    Creates an initialized game of tic tac toe with a unique game_id.

    :return: a newly initialized game status with status code of 201
    """

    # TODO create and persist a unique game

    game = SAMPLE_GAME

    return flask.jsonify(game), 201


@app.route("/games/<int:game_id>", methods=['GET'])
def get_game_status(game_id):
    r"""
    Fetches the current status of the game of tic tac toe.

    :param game_id: unique identifier of tic-tac-toe
    :return: if game exists, return current game status.
                otherwise, return status code 404
    """

    # TODO Look this game up from some place that holds all of the games

    if game_id != 1:
        # This is an unknown game
        return "Game not found", 404

    return flask.jsonify(SAMPLE_GAME)


@app.route("/games/<int:game_id>", methods=['PUT'])
def make_move(game_id):
    r"""
    Makes a move on behalf of a player on the provided game_id.

    :param game_id:
    :return: if game ID exists and the move is valid, return game status after the move is played.
                if the game is not found, return 404 status code
                if the move is a bad request, return 400 status code
    """

    # TODO Look this game up from some place that holds all of the games

    if game_id != 1:
        # This is an unknown game
        return "Game not found", 404

    move = flask.request.get_json()  # Converts input data to JSON
    move = SAMPLE_MOVE  # Example of sample input

    is_valid_move = True  # TODO Validate that this move is valid

    if not is_valid_move:
        return "Invalid move", 400

    # TODO Update the game's board

    game = SAMPLE_GAME

    return flask.jsonify(game)
