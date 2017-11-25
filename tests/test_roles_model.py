import unittest
from flask import current_app
from app import create_app
from app.models.models import db, Roles


class RolesModelTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the application for testing.
        The method 'setUp' simply starts the application in test mode.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.role1 = Roles(title="admin")
        self.role2 = Roles(title="regular")
        self.role1.save()
        self.role2.save()

    def tearDown(self):
        """
        Tear down method.
        This method removes every information related to the test cases.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_model_properties(self):
        self.assertEquals(self.role1.__tablename__, 'roles')
        self.assertFalse(self.role1.id is None)
        self.assertFalse(self.role1.title is None)

        self.assertFalse(self.role2.id is None)
        self.assertFalse(self.role2.title is None)

    def test_uniqueness_of_id_property(self):
        """
        ID property is unique
        Test that shows one id cannot be used for multiple accounts.
        """
        id = Roles.query.first().id
        with self.assertRaises(Exception):
            Roles(id=id, title="member").save()

