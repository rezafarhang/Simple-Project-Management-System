from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    admin_name = db.Column(db.String(50), db.ForeignKey('user.fullname'))
    board_name = db.Column(db.String(50))

class BoardUser(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), primary_key=True)


class BoardCard(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(50))
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    card_field = db.Column(db.String(50))
