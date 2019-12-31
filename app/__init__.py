from flask import Flask, current_app
from config import Config

def creat_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.ancillary import bp as ancillary_bp
    app.register_blueprint(ancillary_bp)

    app.secret_key = Config.APP_SECRET

    return app