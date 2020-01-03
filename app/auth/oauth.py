import json

from flask import redirect
from flask import session
from flask import url_for
from flask import current_app

from functools import wraps
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

from app.auth import bp
from app import db
from app.models import User

oauth = OAuth(current_app)

auth0 = oauth.register(
    'auth0',
    client_id=current_app.config['OAUTH_CLIENT_ID'],
    client_secret=current_app.config['OAUTH_CLIENT_SECRET'],
    api_base_url=current_app.config['OAUTH_API_BASE'],
    access_token_url=current_app.config['OAUTH_API_BASE']+'/oauth/token',
    authorize_url=current_app.config['OAUTH_API_BASE']+'/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_profile' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@bp.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=current_app.config['BASE_URL']+url_for('.oathu_callback_handling'))


@bp.route('/callback')
def oathu_callback_handling():
    oauth.auth0.authorize_access_token()
    resp = oauth.auth0.get('userinfo')
    userinfo = resp.json()

    if db.session.query(User.id).filter_by(id=userinfo['sub']).scalar() is None:
        user = User(userinfo['sub'], username=userinfo['name'],
                    email=userinfo['email'], profileimg=userinfo['picture'])
        db.session.add(user)
        db.session.commit()

    session['jwt_payload'] = userinfo
    session['user_profile'] = {
        'user_id': userinfo['sub'],
        'user_name': userinfo['name'],
        'user_picture': userinfo['picture']
    }
    return redirect(url_for('main.user_dashboard'))


@bp.route('/logout')
def logout():
    session.clear()
    params = {
        'returnTo': url_for('main.home', _external=True),
        'client_id': current_app.config['OAUTH_CLIENT_ID']
    }
    return redirect(auth0.api_base_url+'/v2/logout?'+urlencode(params))