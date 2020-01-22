from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate(compare_type=True)


def creat_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    app.app_context().push()

    db.init_app(app)
    migrate.init_app(app, db=db)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.ancillary import bp as ancillary_bp
    app.register_blueprint(ancillary_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    app.secret_key = Config.APP_SECRET

    return app


from app import models