from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "yusegfugwsefv43543yu"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'elections.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin.login"

# Registring Blueprints goes last!

from electionapp.admin.views import admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix="/admin")

from electionapp.voting.views import voting_blueprint
app.register_blueprint(voting_blueprint, url_prefix="/voting")