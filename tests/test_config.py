import unittest
from flask import current_app
from app import create_app
from app.models.models import db


class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the application for testing.
        The method 'setUp' simply starts the application in test mode.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        Tear down method.
        This method removes every information related to the test cases.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """
        Test that app is in the testing environment.
        """
        self.assertTrue(current_app.config['TESTING'])

