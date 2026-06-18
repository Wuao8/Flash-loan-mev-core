TOKENS_BASE = {
    # core liquidity
    "WETH": "0x4200000000000000000000000000000000000006",
    "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "DAI":  "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",

    # blue chips ecosystem Base
    "AERO": "0x940181A94A35A4569E4529A3CDfB74e38FD98631",
    "cbETH": "0x2Ae3F1Ec7F1F4C74F3F0A1B0A3C8A1A0C0A0000",

    # DeFi layer (liquidity pools heavy)
    "BAL": "0x...BAL_ADDRESS...",
    "UNI": "0x...UNI_ADDRESS...",
    "LINK": "0x...LINK_ADDRESS...",
    "LDO": "0x...LDO_ADDRESS...",

    # Base ecosystem tokens
    "DEGEN": "0x...DEGEN_ADDRESS...",
    "HIGHER": "0x...HIGHER_ADDRESS...",
    "BRETT": "0x...BRETT_ADDRESS...",
    "TOSHI": "0x...TOSHI_ADDRESS...",

    # stable / synthetic variants
    "USDbC": "0xd9aaec86b65d86f6a7b5b1b0b6b2b0b0b0b0b0b0",
}


def get_tokens():
    return TOKENS_BASE
