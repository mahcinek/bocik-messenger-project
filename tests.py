import os
import app
import unittest
import tempfile
from flask import json, jsonify


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_json(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data


if __name__ == '__main__':
    unittest.main()