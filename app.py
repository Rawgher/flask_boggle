from boggle import Boggle
from flask import Flask, render_template, session
boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretpspspspspsp"

@app.route('/')
def home():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('index.html', board=board)