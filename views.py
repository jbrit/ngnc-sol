from flask import Blueprint
from flask_apispec import FlaskApiSpec
from flask_restful import Api

from resources import Wallet, Webhook

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

# API routes -- start
api.add_resource(Wallet, "/<address>")
api.add_resource(Webhook, "/")
# API routes -- end


docs = FlaskApiSpec()

# API docs -- start
docs.register(Wallet, blueprint="api")
docs.register(Webhook, blueprint="api")
# API docs -- end