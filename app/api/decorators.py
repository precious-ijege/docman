from functools import wraps
from flask import g, request, jsonify


def admin_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.role_id != 1:
            return jsonify({
                "message": "UNAUTHORISED ACCESS",
                "status": 401
            }), 401
        return f(*args, **kwargs)
    return decorated_function


def owner_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.id != int(request.path.split('/')[-1]):
            return jsonify({
                "message": "UNAUTHORISED ACCESS",
                "status": 401
            }), 401
        return f(*args, **kwargs)
    return decorated_function


def owner_or_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.id != int(request.path.split('/')[-1]):
            if g.user.role_id != 1:
                return jsonify({
                    "message": "UNAUTHORISED ACCESS",
                    "status": 401
                }), 401
        return f(*args, **kwargs)
    return decorated_function


def create_user_validate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()
        if len(data["first_name"]) < 3 or len(data["last_name"]) < 3:
            return jsonify({
                "message": "FIRST NAME AND LAST NAME MUST BE GREATER THAN 3 CHARACTERS",
                "status": 400
            }), 400
        if len(data["password"]) < 8:
            return jsonify({
                "message": "PASSWORD MUST BE GREATER THAN EIGHT(8) CHARACTERS",
                "status": 400
            }), 400
        return f(*args, **kwargs)
    return decorated_function


def validate_document_create(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()
        if data["user_id"] != g.user.id:
            return jsonify({
                "message": "UNAUTHORISED! YOU CANNOT CREATE A DOCUMENT FOR ANOTHER USER",
                "status": 403
            }), 403
        if len(data["title"]) < 3 or len(data["content"]) < 3:
            return jsonify({
                "message": "DOCUMENT TITLE AND CONTENT MUST BE GREATER THAN 3 CHARACTERS",
                "status": 400
            }), 400
        if data["access"] not in ['public', 'private']:
            return jsonify({
                "message": "DOCUMENT CAN ONLY HAVE ACCESS TYPE OF PUBLIC OR PRIVATE",
                "status": 400
            }), 400
        return f(*args, **kwargs)
    return decorated_function
