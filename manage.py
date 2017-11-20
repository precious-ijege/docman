#!/usr/bin/env python
import os
from app import create_app
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
