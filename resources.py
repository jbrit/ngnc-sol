from functools import wraps
from serializers import WalletSchema
from payments import generate_payment_slug
from flask_apispec import marshal_with
from utils import Resource
import models
from flask import abort, request
from web3 import Web3
from blockchain.handler import mint_tokens


def allow_only_example(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check conditions here
        return func(*args, **kwargs)
    return wrapper
    
class Wallet(Resource):
    @marshal_with(WalletSchema())
    def get(self, address):
        try:
            address = Web3.toChecksumAddress(address)
        except Exception:
            abort(400, 'Invalid address')
        # check if wallet exists and create if not
        wallet = models.Wallet.query.filter_by(address=address).first()
        if wallet is None:
            response = generate_payment_slug(address)["data"]
            wallet = models.Wallet(address=address, payment_page_slug=response["slug"], payment_page_id=response["id"])
            models.db.session.add(wallet)
            models.db.session.commit()
        return wallet


class Webhook(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        raise NotImplementedError
        # webhook to handle the payment completed
        address = "0xcD4bde67fe7C6Eb601d03a35Ea8a55eB2b136965"
        # in kobo
        amount = 5000
        mint_tokens(address, amount)
        return {"success": True}