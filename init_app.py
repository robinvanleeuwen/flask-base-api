from flask import Flask
from flask_jsonrpc import JSONRPC

from endpoints.auth import auth


def create_app():
    app = Flask(__name__)
    api = JSONRPC(app, "/api/v1", enable_web_browsable_api=True)

    endpoints = [
        auth,
    ]

    for ep in endpoints:
        api.register_blueprint(
            app, ep, url_prefix=f"/{ep.name}", enable_web_browsable_api=True
        )

    return app
