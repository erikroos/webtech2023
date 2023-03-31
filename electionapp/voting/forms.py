from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField

class VotingForm(FlaskForm):
    name = StringField("Wat is uw naam?")
    party = SelectField("Op welke partij wilt u stemmen?", choices=[])
    submit = SubmitField("Breng uw stem uit")