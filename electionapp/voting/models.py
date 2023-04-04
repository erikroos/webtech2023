from electionapp import db

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