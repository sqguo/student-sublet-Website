from flask import render_template
from flask import current_app
from flask import redirect
from flask import url_for

from app.main import bp
from app.auth.oauth import requires_auth


@bp.route("/")
def home():
    mapbox_token = current_app.config['MAPBOX_PUBLIC_TOKEN']
    return render_template('home.html', mapbox_token=mapbox_token)


@bp.route('/user/dashboard')
@requires_auth
def user_dashboard():
    return render_template('user/dashboard.html')
