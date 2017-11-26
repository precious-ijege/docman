#!/bin/bash

echo "Installing dependencies"
pip install -r requirements.txt

echo "Applying Migration"
python manage.py db upgrade

echo "Seed Roles data"
python manage.py seed

echo "Starting server"
python manage.py runserver --host=0.0.0.0