from app import db
from datetime import datetime


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    profileimg = db.Column(db.String(200))
    verifiedstu = db.Column(db.Boolean)
    datecreated = db.Column(db.DateTime)
    trustscore = db.Column(db.Integer)
    anonymous = db.Column(db.Boolean)

    def __init__(self, id, username=None, email=None, profileimg=None,
                 anonymous=True, verifiedstu=False, trustscore=1):
        self.id = id
        self.username = username
        self.email = email
        self.profileimg = profileimg
        self.verifiedstu = verifiedstu
        self.datecreated = datetime.utcnow()
        self.trustscore = trustscore
        self.anonymous = anonymous

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

    def set_anonymity(self, anonymous):
        self.anonymous = anonymous

    @property
    def serialize(self):
        if (self.anonymous is True):
            return {
                'anonymous': True
            }
        return {
            'username': self.username,
            'profileimg': self.profileimg,
            'verifiedstu': self.verifiedstu,
            'datecreated': self.datecreated,
            'anonymous': False
        }


class Sublet(db.Model):

    __tablename__ = 'sublets'
    id = db.Column(db.Integer, primary_key=True)
    creatorid = db.Column(db.String(100), db.ForeignKey('users.id'))
    datecreated = db.Column(db.DateTime)
    datemodified = db.Column(db.DateTime)
    title = db.Column(db.String(100))
    address = db.Column(db.String(100))
    postalcode = db.Column(db.String(6))
    avgrating = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    profileimg = db.Column(db.String(200))
    description = db.Column(db.String(200))
    management = db.Column(db.String(30))

    def __init__(self, creatorid, latitude, longitude, title,
                 address=None, profileimg=None, description=None,
                 avgrating=None, postalcode=None, management=None):
        self.creatorid = creatorid
        self.title = title
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.postalcode = postalcode
        self.avgrating = avgrating
        self.profileimg = profileimg
        self.description = description
        self.datecreated = datetime.utcnow()
        self.management = management

    def __repr__(self):
        return '<Sublet {} at {}, {}>'.format(
            self.id, self.longitude, self.latitude)

    def set_avgrating(self, avgrating):
        self.avgrating = avgrating

    def set_description(self, description):
        self.description = description
        self.datemodified = datetime.utcnow()

    def set_position(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.datemodified = datetime.utcnow()

    def set_title(self, title):
        self.title = title

    def set_address(self, address):
        self.address = address

    def set_postalcode(self, postalcode):
        self.postalcode = postalcode

    def set_management(self, management):
        self.management = management

    def set_profileimg(self, profileimg):
        self.profileimg = profileimg

    @property
    def serialize(self):
        return {
            'id': self.id,
            'datecreated': self.datecreated,
            'datemodified': self.datemodified,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'description': self.description,
            'avgrating': self.avgrating,
            'profileimg': self.profileimg
        }


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
        self.datecreated = datetime.utcnow()

    def __repr__(self):
        return '<Review {} by {}>'.format(self.id, self.authorid)

    def set_content(self, content):
        self.content = content
        self.datemodified = datetime.utcnow()

    def set_rating(self, rating):
        self.rating = rating
        self.datemodified = datetime.utcnow()


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
        self.datecreated = datetime.utcnow()

    def __repr__(self):
        return '<Review {} by {}>'.format(self.id, self.authorid)

    def set_content(self, content):
        self.content = content
        self.datemodified = datetime.utcnow()
