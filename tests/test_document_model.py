import unittest
from app import create_app
from app.models.models import db, Roles, Users, Documents


class DocumentModelTestCase(unittest.TestCase):
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

    def tearDown(self):
        """
        Tear down method.
        This method removes every information related to the test cases.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_document(self):
        document = Documents(title='test', content='testing document', access='public', user_id=1)
        document.save()
        query_document = Documents.query.get(1)
        self.assertFalse(query_document is None)
        self.assertFalse(query_document.id is None)
        self.assertFalse(query_document.title is None)
        self.assertTrue(query_document.title == 'test')

