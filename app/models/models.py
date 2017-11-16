from flask import current_app
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CRUDMixin(object):
    """
    Define the Create,Read, Update, Delete mixin.
    Instantiate a mixin to handle save, delete and also handle common model
    columns and methods.
    """

    date_created = db.Column(
        db.DateTime, default=datetime.now(), nullable=False)

    def save(self):
        """
        Save to database.
        Save instance of the object to database and commit.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete from database.
        Deletes instance of an object from database
        """
        db.session.delete(self)
        db.session.commit()

    def hash_password(self, password):
        """
        Hash user password.
        Passwords shouldn't be stored as string so we hash them.
        """
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        """
        Verify password.
        Use the pwd_context to decrypt the password hash and confirm if it
        matches the initial password set by the user.
        """
        return check_password_hash(self.password, password)


class Roles(CRUDMixin, db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Roles %r>' % self.title


class Users(CRUDMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    roles = db.relationship('Roles',
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<Users %r>' % self.first_name

    def generate_auth_token(self, expiration=600):
        """
        Generate token.
        This function generates a token to be used by the user for requests.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """
        Verify token.
        Verify that the token is valid and return the user id.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None

            # valid token, but expired
        except BadSignature:
            return None

            # invalid token
        user = Users.query.get(data['id'])
        return user


class Documents(CRUDMixin, db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String, nullable=False)
    access = db.Column(db.String(20), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('Users',
                            backref=db.backref('documents', lazy='dynamic'))

    def __repr__(self):
        return '<Documents %r>' % self.title

