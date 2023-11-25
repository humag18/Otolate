from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/otolate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, default=0)
    s3 = db.Column(db.Integer, default=0)
    challenges = db.relationship('Challenge', secondary='user_challenge', back_populates='users')

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    context = db.Column(db.String(255), nullable=False)
    date_upload = db.Column(db.DateTime, nullable=False)
    delay = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    users = db.relationship('User', secondary='user_challenge', back_populates='challenges')

# Table d'association User-Challenge
user_challenge = db.Table('user_challenge',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id'), primary_key=True),
    db.Column('path', db.String(255)),
    db.Column('date_upload', db.DateTime),
    db.Column('likes', db.Integer)
)

migrate = Migrate(app, db)