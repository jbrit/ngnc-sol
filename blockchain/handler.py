import os

from web3 import Web3
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from blockchain.abis import NGNC_ABI

private_key = os.environ["POLYGON_PRIVATE_KEY"]


w3 = Web3(Web3.HTTPProvider("https://matic-mumbai.chainstacklabs.com"))
w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)

def get_ngnc_contract():
    return w3.eth.contract(address="0x9c15A02479af310Afe579A058e5dc9797243103f", abi=NGNC_ABI)

def mint_tokens(address, amount):
    nonce = w3.eth.get_transaction_count('0x176AF24f7eC865Cba4Eef2f4a1523F61D728Bfd1')
    gas_price = w3.eth.generate_gas_price()
    mint_tokens_tx = get_ngnc_contract().functions.mintTokens(address, amount).buildTransaction({
        'chainId': 80001,
        'nonce': nonce,
        'gasPrice': gas_price,
        'gas': 200000,
    })
    signed_txn = w3.eth.account.sign_transaction(mint_tokens_tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt