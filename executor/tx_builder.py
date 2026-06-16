from web3 import Web3
from config import BASE_RPC_URL


w3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))


def build_simple_swap_tx(from_address, to_address, data, value=0):

    tx = {
        "from": from_address,
        "to": to_address,
        "data": data,
        "value": value,
        "gas": 400000,
        "gasPrice": w3.to_wei("0.05", "gwei"),
        "nonce": w3.eth.get_transaction_count(from_address),
        "chainId": 8453  # Base
    }

    return tx
