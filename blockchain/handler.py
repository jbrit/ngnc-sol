import base58
import os

from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import get_associated_token_address
from spl.token.client import Token

from solana.rpc.commitment import Confirmed
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.keypair import Keypair


private_key = os.environ["SOLANA_PRIVATE_KEY"]

client = Client(endpoint="https://api.devnet.solana.com", commitment=Confirmed)
owner = Keypair.from_seed(base58.b58decode(private_key))

def get_or_create_ata(token: Token, address: PublicKey, mint: PublicKey):
    # TODO: check if ata initialized then create instead
    try:
        ata = token.create_associated_token_account(owner=address)
    except Exception:
        ata = get_associated_token_address(owner=address, mint=mint)
    return ata
    

def mint_tokens(address: str, amount: int):
    token = Token(
        conn=client,
        pubkey=PublicKey("BBPQBEAL4uMvyL99Ms6r2vqaVst4RtgZF8Xgnut2x1Lh"),
        payer=owner,
        program_id=TOKEN_PROGRAM_ID,
    )
    ata = get_or_create_ata(token, PublicKey(address), PublicKey("BBPQBEAL4uMvyL99Ms6r2vqaVst4RtgZF8Xgnut2x1Lh"))
    tx = token.mint_to_checked(
        dest=ata,
        mint_authority=owner,
        amount=amount,
        decimals=2
    )
    signature = tx["result"]
    return signature


def create_mint():
    # creating token with 2 decimals here
    token = Token.create_mint(
        conn=client,
        payer=owner,
        mint_authority=owner.public_key,
        decimals=2,
        program_id=TOKEN_PROGRAM_ID,
    )
    print(f" New token deployed to {token.pubkey}")