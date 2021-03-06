from flask import Flask, request, render_template, jsonify, session
# from flask_debugtoolbar import DebugToolbarExtension
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# debug = DebugToolbarExtension(app)

# The boggle games created, keyed by game id
games = {}


@app.route("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.route("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify(gameId=game_id, board=game.board)


@app.route("/api/score-word", methods=["POST"])
def score_word():
    """ check if the word is valid on board and if it's in dictionary, 
    returns not-word, not-on-board or ok """
    game_id = request.json["gameId"]
    word = request.json["word"].upper()
    game = games[game_id]
    if not game.is_word_in_word_list(word):
        result = "not-word"
    elif not game.check_word_on_board(word):
        result = "not-on-board"
    else:
        result = "ok"
    return jsonify(result=result)
