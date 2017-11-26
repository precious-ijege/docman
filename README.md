# docman
Docman is a full stack document management system, complete with roles and privileges. It creates a restful API for users to create and manage documents and it also provides admin priviledges.

## Development
* [Flask](http://flask.pocoo.org/) - Flask is a BCD licensed microframework for Python based on Werkzeug and Jinja 2.
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) - This an extension that handles SQLAlchemy database migrations for Flask applications using Alembic. The database operations are made available through the Flask command-line interface.
* [Flask-Script](https://flask-script.readthedocs.io/en/latest/) - This extension provides support for writing external scripts in Flask. This includes running a development server, a customized Python shell, scripts to set up a database and other command-line tasks that belong outside the web application itself.
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/) - This extension help to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.
* [Python-Env](https://github.com/mattseymour/python-env) - This library allows the saving of environment variables in .env and loaded when the application runs.

## Application Features
###### User Authentication
Users are authenticated and validated using an `itsdangerous` token. Generating tokens on login ensures each account is unique to a user and can't be accessed by an authenticated user.
    
## API Documentation
Docman exposes its data via an Application Programming Interface (API), so developers can interact in a programmatic way with the application. This document is the official reference for that functionality.

### API Resource Endpoints

URL Prefix = `http://sample_domain/api/` where sample domain is the root URL of the server HOST.


| EndPoint                                 | Functionality                 | Access|
| -----------------------------------------|-----------------------------|:-------------:|
| **GET** `/`        | Home page  |    User      |
| **POST** `/rolesr`            | Creates a new role              |    Admin     |
| **GET** `/roles`        | Returns all Roles  |    Admin      |
| **POST** `/users`           | Creates a new user |    User    |
| **POST** `/users/login`           | Log in a user |    User    |
| **DELETE** `/users/<int:user_id>`         | Deletes a user  |    User    |
| **PUT** `/users/<int:user_id>`         | Edits a user  |    User    |
| **GET** `/users`         | Returns all users  |    Admin    |
| **GET** `/search/users`         | Search for a user  |    Admin    |
| **POST** `/documents         `            | Creates a document  |    User      |
| **GET** `/myDocuments/<int:user_id>`         | Returns a users documents  |    User    |
| **GET** `/documents/public/<int:user_id>`         | Returns all public Document  |    User    |
| **GET** `/search/documents`         | Search for a public document |    User    |
| **GET** `/search/myDocuments`         | Search for a personal document  |    User    |
| **GET** `/documents/<int:user_id>`         | Returns a single document  |    User    |


 ### Running Tests
1. Navigate to the project directory.
2. Run `python manage.py test` to run test and check coverage.

## License

This project is authored by **Ijege Precious** (precious.ijege@andela.com) and is licensed for your use, modification and distribution under the **MIT** license. 

[MIT][license] © [andela-pijege][author]

<!-- Definitions -->

[license]: LICENSE

[author]: andela-pijege

