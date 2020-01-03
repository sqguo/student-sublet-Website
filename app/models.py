from app import db
from datetime import datetime


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    profileimg = db.Column(db.String(200))
    verifiedstu = db.Column(db.Boolean)
    datecreated = db.Column(db.String(50))
    trustscore = db.Column(db.Integer)

    def __init__(self, id, username=None, email=None, profileimg=None,
                 verifiedstu=False, trustscore=1):
        self.id = id
        self.username = username
        self.email = email
        self.profileimg = profileimg
        self.verifiedstu = verifiedstu
        self.datecreated = datetime.utcnow()
        self.trustscore = trustscore

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def set_username(self, username):
        self.username = username

    def set_verifiedstu(self, verifiedstu):
        self.verifiedstu = verifiedstu

    def set_profileimg(self, profileimg):
        self.profileimg = profileimg

    def set_trustscore(self, trustscore):
        self.trustscore = trustscore
