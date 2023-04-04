from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# 1. The app
app = Flask(__name__)
app.config['SECRET_KEY'] = "yusegfugwsefv43543yu"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'elections.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. The database
db = SQLAlchemy(app)

# 3. The login manager (needed when you want to use current_user in your templates etc.)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin.login"

# 4. Registring blueprints goes last! (blueprints are used to put routes (views) and forms that belong together into separate sections)
from electionapp.admin.views import admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix="/admin")

from electionapp.voting.views import voting_blueprint
app.register_blueprint(voting_blueprint, url_prefix="/voting")