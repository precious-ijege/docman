import unittest
from app import create_app
from app.models.models import db, Roles, Users


class UsersModelTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the application for testing.
        The method 'setUp' simply starts the application in test mode.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.admin = Roles(title='admin')
        self.admin.save()
        self.regular = Roles(title='regular')
        self.regular.save()
        self.admin_user = Users(
            first_name='ghost', last_name='messi',
            email='ghost.messi@gmail.com',
            password='password', role_id=1
        )
        self.admin_user.hash_password(self.admin_user.password)
        self.admin_user.save()
        self.regular_user = Users(
            first_name='john',last_name='james',
            email='john.james@gmail.com',
            password='password', role_id=2
        )
        self.regular_user.hash_password(self.regular_user.password)
        self.regular_user.save()

    def tearDown(self):
        """
        Tear down method.
        This method removes every information related to the test cases.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hash_exist(self):
        """
        Test that the hash password function exists.
        """
        self.assertTrue(self.regular_user.hash_password is not None)

    def test_password_is_hashed(self):
        """
        Test password.
        Test the password is actually hashed.
        """
        self.assertTrue(self.regular_user.password != 'password')
        self.assertTrue(self.admin_user.password != 'password')

    def test_password_hash_is_not_the_same(self):
        """
        Test password hash.
        Test identical passwords return disimilar password hashes.
        """
        self.assertFalse(self.admin_user.password == self.regular_user.password)

    def test_verify_password(self):
        """
        Test the hashed password.
        Check if the hashed password is the same as the password when it has
        been decrypted.
        """
        self.assertTrue(self.admin_user.verify_password('password'))
        self.assertTrue(self.regular_user.verify_password('password'))

    def test_uniqueness_of_email_property(self):
        """
        email property is unique
        Test that shows one email cannot be used for multiple accounts.
        """
        email = Users.query.first().email
        with self.assertRaises(Exception):
            new_user = Users(first_name='sammy',last_name='sammy',
            email=email, password='password', role_id=2)
            new_user.save()

