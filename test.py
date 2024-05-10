from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Setting up before running the tests"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Checking to see if the session is set up properly"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('plays'))
            self.assertIn(b'High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):
        """Test if a valid word is on the board"""

        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"]]
        response = self.client.get('/check-word?word=dog')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is somewhere in the dictionary"""

        self.client.get('/')
        response = self.client.get('/check-word?word=bad')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Testing what happens if a word is not on the board"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=gibberishfsddflih')
        self.assertEqual(response.json['result'], 'not-word')