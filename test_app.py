from unittest import TestCase

from app import app, games

import json

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            # test that you're getting a template
            
            self.assertIn('id="boggle_game_board"', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.get('/api/new-game')
            response_data = response.json

            # test that gameId is a string
            self.assertIsInstance(response_data["gameId"], str)

            # test that board is a list of a list
            self.assertIsInstance(response_data["board"], list)
            self.assertIsInstance(response_data["board"][0], list)

            # test that new game is stored in the games dictionary
            self.assertIn(response_data["gameId"], games.keys())

    def test_api_score_word(self):
        """ Test scoring a word """
        with self.client as client:
            response = client.get('/api/new-game')
            game_id = response.json["gameId"]
            game = games[game_id]
            game.board = [
                ['A', 'P', 'U', 'T', 'E'],
                ['G', 'C', 'C', 'S', 'C'],
                ['S', 'L', 'T', 'R', 'N'],
                ['M', 'D', 'L', 'N', 'L'],
                ['T', 'N', 'G', 'U', 'S']]

            def _post_word_result(word):
                """ takes in a word str and makes ajax post request, and return
                    the result string from response"""
                response = client.post("/api/score-word",
                                       json={"gameId": game_id, "word": word}))
                result = response.json["result"]
                return result
            # test for different words on the same board
            self.assertEqual(_post_word_result("CUTE"), "ok")
            self.assertEqual(_post_word_result("SLUNG"), "ok")
            self.assertEqual(_post_word_result("DFDFD"), "not-word")
            self.assertEqual(_post_word_result("HELLO"), "not-on-board")