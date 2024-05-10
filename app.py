from boggle import Boggle
from flask import Flask, render_template, session, request, jsonify
boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretpspspspspsp"

@app.route('/')
def home():
    """ Initializing the game board and passing relevant information through to the template"""
    
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)
    return render_template('index.html', board=board, highscore=highscore, plays=plays)

@app.route("/check-word")
def check_word():
    """Checking to see if the user's guess is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Holds the current score and continues the game. Posts the high score at the end of play"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)

    session['plays'] = plays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)