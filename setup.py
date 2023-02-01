from flask import Flask
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_restful import abort
from flask_migrate import Migrate
from webargs.flaskparser import parser
from config import app_config
from views import api_blueprint, docs
from models import db

# This error handler is necessary for usage with Flask-RESTful
# pylint: disable=unused-argument
@parser.error_handler
def handle_request_parsing_error(err, req, schema, **kwargs):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(422, errors=err.messages)


migrate = Migrate()

def create_app():

    sentry_sdk.init(
        dsn="https://30ba31ac051a426b8e5f2f949699c7d4@o971311.ingest.sentry.io/4504241627070464",
        integrations=[
            FlaskIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )
