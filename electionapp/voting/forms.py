from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired

class VotingForm(FlaskForm):
    name = StringField("Wat is uw naam?", validators=[InputRequired()])
    party = SelectField("Op welke partij wilt u stemmen?", choices=[])
    submit = SubmitField("Breng uw stem uit")