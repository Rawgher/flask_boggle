from boggle import Boggle
from flask import Flask

boggle_game = Boggle()

app = Flask(__name__)

@app.route('/')
def home():
    return 'Test'