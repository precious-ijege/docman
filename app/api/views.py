from flask import jsonify, g
from . import api
from ..models.models import Roles, Users, Documents
from helper import to_json, user_to_json, document_to_json
from flask import current_app, request
from ..models import models
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


@api.before_request
def verify_auth_token():
    """
    Verify token.
    Verify that the token is valid and return the user id.
    """
    list_of_paths = ["/", "/api/users/login"]
    if (request.path in list_of_paths) or (request.path == "/api/users" and request.method == "POST"):
        return None
    else:
        if not request.headers.has_key("Token"):
            return '<h1>Empty Token</h1>'
        token = request.headers['Token']
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return '<h1>Invalid token</h1>'

            # valid token, but expired
        except BadSignature:
            return '<h1>Invalid token</h1>'

            # invalid token
        g.user = models.Users.query.get(data['id'])
        return None


@api.route('/', methods=['GET'])
def index():
    return '<h1>welcome to Docman API Bitches</h1>', 200


@api.route('/api/roles', methods=['POST'])
def create_role():
    """
    Create a new role.
    Add a new role and returns the role for the user to view
    """
    title = Roles(title=request.json['title'])
    title.save()
    return jsonify({
        "message": "{} has been created"
                   .format(request.json['title']),
        "status": 201
    }), 201


@api.route('/api/roles', methods=['GET'])
def get_all_roles():
    """
    Get all the created roles Lists.
    Displays a json of all the created roles List .
    """
    roles = Roles.query.all()
    all_roles = [to_json(role) for role in roles]
    return jsonify({
        "Roles": all_roles,
        "status": 200
    }), 200

# Users routes


@api.route('/api/users/login', methods=['POST'])
def user_login():
    if request.json['email'] == '' or request.json['password'] == '':
        return jsonify({
            "message": 'Enter valid email and password',
            "status": 400
        }), 400
    else:
        user = Users.query.filter_by(email=request.json['email']).first()
        if not (user and user.verify_password(request.json['password'])):
            return jsonify({
                "message": 'Incorrect Login details',
                "status": 400
            }), 400
        else:
            token = user.generate_auth_token()
            return jsonify({
                "message": 'Login successful',
                "status": 200,
                "token": token
            }), 200


@api.route('/api/users', methods=['POST'])
def create_user():
    """
    Create a new user.
    Add a new user and returns the user for the user to view
    """
    user = Users(first_name=request.json['first_name'],
        last_name=request.json['last_name'],
        email=request.json['email'],
        role_id=request.json['role_id'])
    user.hash_password(request.json['password'])
    user.save()
    return jsonify({
        "message": "{} {} has been created"
                   .format(request.json['first_name'], request.json['last_name']),
        "status": 201
    }), 201


@api.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """Get a particular user with it's ID and delete it."""
    user = Users.query.get(id)
    user.delete()
    return jsonify({
        "message": "The user {} {} has been deleted.".format(user.first_name, user.last_name),
        "status": 200
    }), 200


@api.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = Users.query.get(id)
    user.first_name = request.json.get('first_name', user.first_name)
    user.last_name = request.json.get('last_name', user.last_name)
    user.email = request.json.get('email', user.email)
    user.password = request.json.get('password', user.password)
    user.save()
    return jsonify({
        "message": "The user {} {} has been updated.".format(user.first_name, user.last_name),
        "status": 200
    }), 200


@api.route('/api/users', methods=['GET'])
def get_all_users():
    """
    Get all the created roles Lists.
    Displays a json of all the created roles List .
    """
    users = Users.query.all()
    all_users = [user_to_json(user) for user in users]
    return jsonify({
        "Roles": all_users,
        "status": 200
    }), 200


# documets routes


@api.route('/api/documents', methods=['POST'])
def create_document():
    """
    Create a new document.
    Add a new document and returns a success message
    """
    document = Documents(title=request.json['title'],
        content=request.json['content'],
        access=request.json['access'],
        user_id=request.json['user_id'])
    document.save()
    return jsonify({
        "message": "Document created successfully",
        "status": 201
    }), 201


@api.route('/api/documents/<int:id>', methods=['DELETE'])
def delete_document(id):
    """Get a particular document with it's ID and delete it."""
    document = Documents.query.get(id)
    document.delete()
    return jsonify({
        "message": "Document deleted successfully",
        "status": 200
    }), 200


@api.route('/api/documents/<int:user_id>', methods=['GET'])
def get_users_documents(user_id):
    documents = Documents.query.filter_by(user_id=user_id).all()
    my_documents = [document_to_json(document) for document in documents]
    return jsonify({
        "documents": my_documents,
        "status": 200
    }), 200


@api.route('/api/documents/public', methods=['GET'])
def get_public_documents():
    documents = Documents.query.filter_by(access='public').all()
    public_documents = [document_to_json(document) for document in documents]
    return jsonify({
        "documents": public_documents,
        "status": 200
    }), 200

