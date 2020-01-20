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


class Sublet(db.Model):

    __tablename__ = 'sublets'
    id = db.Column(db.Integer, primary_key=True)
    creatorid = db.Column(db.String(100), db.ForeignKey('users.id'))
    datecreated = db.Column(db.DateTime)
    datemodified = db.Column(db.DateTime)
    avgrating = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    profileimg = db.Column(db.String(200))
    description = db.Column(db.String(200))

    def __init__(self, id, creatorid, latitude=None, longitude=None,
                 profileimg=None, description=None, avgrating=None):
        self.creatorid = creatorid
        self.latitude = latitude
        self.longitude = longitude
        self.avgrating = avgrating
        self.profileimg = profileimg
        self.description = description
        self.datecreated = datetime.utcnow

    def __repr__(self):
        return '<Sublet {} at {}, {}>'.format(
            self.id, self.longitude, self.latitude)

    def set_avgrating(self, avgrating):
        self.avgrating = avgrating

    def set_description(self, description):
        self.description = description

    def set_profileimg(self, profileimg):
        self.profileimg = profileimg


class Review(db.Model):

    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    authorid = db.Column(db.String(100), db.ForeignKey('users.id'))
    subletid = db.Column(db.Integer)
    datecreated = db.Column(db.DateTime)
    datemodified = db.Column(db.DateTime)
    rating = db.Column(db.Integer)

    def __init__(self, authorid, rating, content=None):
        self.authorid = authorid
        self.rating = rating
        self.content = content
        self.datecreated = datetime.utcnow

    def __repr__(self):
        return '<Review {} by {}>'.format(self.id, self.authorid)

    def set_content(self, content):
        self.content = content
        self.datemodified = datetime.utcnow

    def set_rating(self, rating):
        self.rating = rating
        self.datemodified = datetime.utcnow


class Reply(db.Model):

    __tablename__ = "replies"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    reviewid = db.Column(db.Integer, db.ForeignKey('reviews.id'))
    authorid = db.Column(db.String(100), db.ForeignKey('users.id'))
    datecreated = db.Column(db.DateTime)
    datemodified = db.Column(db.DateTime)

    def __init__(self, authorid, reviewid, content=None):
        self.authorid = authorid
        self.reviewid = reviewid
        self.content = content
        self.datecreated = datetime.utcnow

    def __repr__(self):
        return '<Review {} by {}>'.format(self.id, self.authorid)

    def set_content(self, content):
        self.content = content
        self.datemodified = datetime.utcnow
