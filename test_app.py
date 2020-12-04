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
            response_data = response.get_data(as_text=True)
            JSON_data = json.loads(response_data)
            
            # test that gameId is a string
            self.assertIsInstance(JSON_data["gameId"], str)

            # test that board is a list of a list
            self.assertIsInstance(JSON_data["board"], list)
            self.assertIsInstance(JSON_data["board"][0], list)

            # test that new game is stored in the games dictionary
            self.assertIn(JSON_data["gameId"], games.keys())
