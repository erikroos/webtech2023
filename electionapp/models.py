from electionapp import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Voter(db.Model):
    __tablename__ = 'voters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

class Party(db.Model):
    __tablename__ = 'parties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)

    voter_id = db.Column(db.Integer, db.ForeignKey('voters.id'))
    voter = db.relationship('Voter', backref='Vote', uselist=False)

    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'))
    party = db.relationship('Party', backref='Vote', uselist=False)

    def __init__(self, voter_id, party_id):
        self.voter_id = voter_id
        self.party_id = party_id

    def __repr__(self):
        return f"Stemmer {self.voter.name} heeft gestemd op {self.party.name}"