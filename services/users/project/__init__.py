# services/users/project/__init__.py


import os

from flask import Flask  # nuevo
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS  # nuevo
from flask_migrate import Migrate  # new
from flask_bcrypt import Bcrypt  # nuevo


# instantiate the db
db = SQLAlchemy()
toolbar = DebugToolbarExtension()
cors = CORS()  # nuevo
migrate = Migrate()  # nuevo
bcrypt = Bcrypt()  # nuevo


# nuevo
def create_app(script_info=None):

    # instanciado la  app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # configurar la extension
    db.init_app(app)
    toolbar.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)  # nuevo
    bcrypt.init_app(app)  # nuevo

    # registrar blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # contexto shell para flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
