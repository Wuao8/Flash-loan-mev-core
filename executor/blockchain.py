from web3 import Web3

BASE_RPC = "https://mainnet.base.org"

w3 = Web3(Web3.HTTPProvider(BASE_RPC))

CONTRACT_ADDRESS = "0x18A2d935Bcb84E24e8f8685D3445589016a5afAd"

# ABI minimale del tuo contratto
ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "symbol", "type": "string"},
            {"internalType": "uint256", "name": "grossProfit", "type": "uint256"},
            {"internalType": "uint256", "name": "gasCost", "type": "uint256"},
            {"internalType": "uint256", "name": "flashFee", "type": "uint256"}
        ],
        "name": "executeArbitrage",
        "outputs": [{"internalType": "int256", "name": "", "type": "int256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
