from flask import Flask, render_template, flash, redirect, url_for, session
from forms import VotingForm
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "yusegfugwsefv43543yu"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'elections.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

### CLASSES:

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

### ROUTES:

@app.route('/')
def index():
    if not 'voted' in session.keys():
        session['voted'] = 0

    form = VotingForm()
    form.party.choices = [(p.id, p.name) for p in Party.query.order_by('name')]

    return render_template('vote.html', form=form)

@app.route('/vote', methods=['post'])
def vote():
    form = VotingForm()
    form.party.choices = [(p.id, p.name) for p in Party.query.order_by('name')]

    if form.validate_on_submit() and form.name.data != "":
        session['voted'] = 1
        flash(f"Bedankt {form.name.data}, voor uw stem!")

        # Add to db
        voter = Voter(form.name.data)
        db.session.add(voter)
        db.session.commit()
        voter_id = voter.id
        party_id = form.party.data
        vote = Vote(voter_id, party_id)
        db.session.add(vote)
        db.session.commit()

        return redirect(url_for("thanks"))
    else:
        flash("Ongeldige stem")
        return redirect(url_for("fail"))

@app.route('/thanks')
def thanks():
    all_votes = Vote.query.all()
    return render_template("thanks.html", votes=all_votes)

@app.route('/fail')
def fail():
    return render_template("fail.html")

if __name__ == "__main__":
    app.run(debug=True)