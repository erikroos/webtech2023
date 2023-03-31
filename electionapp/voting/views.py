from electionapp import db
from flask import Blueprint, render_template, redirect, request, url_for, flash
from electionapp.models import Vote, Party, Voter
from electionapp.voting.forms import VotingForm

voting_blueprint = Blueprint('voting', __name__, template_folder='templates')

@voting_blueprint.route('/form')
def form():
    form = VotingForm()
    form.party.choices = [(p.id, p.name) for p in Party.query.order_by('name')]

    return render_template('vote.html', form=form)

@voting_blueprint.route('/vote', methods=['post'])
def vote():
    form = VotingForm()
    form.party.choices = [(p.id, p.name) for p in Party.query.order_by('name')]

    if form.validate_on_submit() and form.name.data != "":
        # Add to db
        voter = Voter(form.name.data)
        db.session.add(voter)
        db.session.commit()
        voter_id = voter.id
        party_id = form.party.data
        vote = Vote(voter_id, party_id)
        db.session.add(vote)
        db.session.commit()

        flash(f"Bedankt {form.name.data}, voor uw stem!")

        return redirect(url_for("voting.thanks"))
    else:
        flash("Ongeldige stem")
        return redirect(url_for("voting.fail"))

@voting_blueprint.route('/thanks')
def thanks():
    return render_template("thanks.html")

@voting_blueprint.route('/fail')
def fail():
    return render_template("fail.html")