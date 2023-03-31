from electionapp import db
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from electionapp.models import User, Vote
from electionapp.admin.forms import LoginForm, RegistrationForm

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

@admin_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('U bent nu uitgelogd')
    return redirect(url_for('index'))

@admin_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('U bent succesvol ingelogd')
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('admin.votes')
                return redirect(next)
    return render_template('login.html', form=form)

@admin_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Add to db
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Bedankt voor de registratie. Er kan nu ingelogd worden!')
        return redirect(url_for('admin.login'))
    return render_template('register.html', form=form)

@admin_blueprint.route('/votes')
@login_required
def votes():
    all_votes = Vote.query.all()
    return render_template('votes.html', votes=all_votes)