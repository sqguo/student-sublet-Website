from flask import render_template
from flask import redirect
from flask import url_for
from app import db
from app.main import bp
from app.models import User
from app.auth.oauth import requires_auth


@bp.route("/")
def home():
    return render_template('home.html')


@bp.route("/countusers")
def count_users():
    num = User.query.count()
    return str(num)


@bp.route('/user/dashboard')
@requires_auth
def user_dashboard():
    return render_template('user/dashboard.html')
