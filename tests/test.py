import unittest

from flask import current_app  # Import app from flask

from app import create_app
from app import db, User, Ticket
from config import config


class TestCase(unittest.TestCase):
    # Executes actions before executing test
    def setUp(self):
        # Obtain configuration
        config_class = config['test']
        # Generate app
        self.app = create_app(config_class)
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.id = 1

    # Executions actions after executing test
    def tearDown(self):
        # Deletes all tables after every test
        db.session.remove()
        db.drop_all()

        self.app_context.pop()

    def test_demo(self):
        self.assertTrue(1 == 1)

    def test_user_exists(self):
        user = User.get_by_id(self.id)
        # On this database we still have no users
        self.assertTrue(user is None)

    def test_create_user(self):
        user = User.create_element('username', 'email@gmail.com', 'password')
        self.assertTrue(user.id == self.id)