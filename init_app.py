import os

from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from endpoints.account import account
from endpoints.auth import auth


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ.get("APP_SETTINGS"))
    api = JSONRPC(app, "/api/v1", enable_web_browsable_api=True)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    endpoints = [
        auth,
        account,
    ]

    for ep in endpoints:
        api.register_blueprint(
            app, ep, url_prefix=f"/{ep.name}", enable_web_browsable_api=True
        )

    return app
