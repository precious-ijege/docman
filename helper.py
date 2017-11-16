"""Define helper functions to be used here."""


def to_json(role):
    """Convert SQL queries to actual dictionaries."""
    result = {
        "id": role.id,
        "title": role.title,
        "date_created": role.date_created
    }
    return result


def user_to_json(user):
    """Convert SQL queries to actual dictionaries."""
    result = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role_id": user.role_id,
        "date_created": user.date_created
    }
    return result


def document_to_json(document):
    """Convert SQL queries to actual dictionaries."""
    result = {
        "id": document.id,
        "title": document.title,
        "content": document.content,
        "access": document.access,
        "user_id": document.user_id,
        "date_created": document.date_created
    }
    return result

