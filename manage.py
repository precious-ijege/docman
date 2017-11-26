#!/usr/bin/env python
import os
from app import create_app
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import db
from app.models.models import Roles


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app)


@manager.command
def seed():
    " Seeds the database with predefined roles"
    admin_role = Roles(title="admin")
    regular_role = Roles(title="regular")
    db.session.add_all([admin_role, regular_role])
    db.session.commit()


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
