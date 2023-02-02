import base58
import os

from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import InitializeMintParams, initialize_mint
from spl.token.client import Token

from solana.rpc.commitment import Confirmed
from solana.rpc.api import Client
from solana.keypair import Keypair
# from solders.keypair import Keypair

private_key = os.environ["SOLANA_PRIVATE_KEY"]

client = Client(endpoint="https://api.devnet.solana.com", commitment=Confirmed)
owner = Keypair.from_seed(base58.b58decode(private_key))

def mint_tokens(address, amount):
    # similar pattern?
    params = InitializeMintParams(
        decimals=2,
        program_id=TOKEN_PROGRAM_ID,
        mint=owner.public_key,
        mint_authority=owner.public_key,
        freeze_authority=owner.public_key,
    )
    tx = initialize_mint(params)
    pass


def create_mint():
    # creating token with 2 decimals here
    token = Token.create_mint(
        conn=client,
        payer=owner,
        mint_authority=owner.public_key,
        decimals=2,
        program_id=TOKEN_PROGRAM_ID,
        skip_confirmation=False
    )
    print(f" New token deployed to {token.pubkey}")