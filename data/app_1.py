from flask import Flask, render_template, url_for, request, session, redirect, send_from_directory, send_file
from cfApi import *
from random import randint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# from flask_ngrok import run_with_ngrok


interfaces = [
    'name',
    'other',
    'description',
    'urls',
    'paste',
    'user'
]
app = Flask(__name__)
# run_with_ngrok(app)
app.config['SECRET_KEY'] = generate_password_hash('Alfred Hitchcock')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://////Users\honor\OneDrive\Рабочий стол\algoblog-project\app.py'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Algo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    other = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    urls = db.Column(db.Text, nullable=False)
    paste = db.Column(db.String, unique=True, nullable=False)
    user = db.Column(db.String, nullable=False)


def updateDB():
    A = Algo()
    A.name = session['algo']['name']
    A.other = session['algo']['other']
    A.description = session['algo']['description']
    A.urls = session['algo']['urls']
    A.paste = session['algo']['paste']
    A.user = session['algo']['user']
    db.session.add(A)
    db.session.commit()


def changeDB(note):
    db.session.merge(note)
    db.session.commit()


def deleteDB(note):
    db.session.delete(note)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
