TOKENS_BASE = {

    # =========================
    # CORE LIQUIDITY (MANDATORY)
    # =========================
    "WETH": "0x4200000000000000000000000000000000000006",
    "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "DAI":  "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
    "USDbC": "0xd9aaec86b65d86f6a7b5b1b0b6b2b0b0b0b0b0b0",

    # =========================
    # BLUE CHIP / MAJOR DEFI
    # =========================
    "cbETH": "0x2Ae3F1Ec7F1F4C74F3F0A1B0A3C8A1A0C0A0000",
    "AERO":  "0x940181A94A35A4569E4529A3CDfB74e38FD98631",
    "BAL":   "0x4158734D47Fc9692176B5085E0F52ee0Da5d47F1",
    "UNI":   "0xc3De830EA07524a0761646a6a4e4be0e114a3C83",
    "LINK":  "0x88Fb150BDc53A65fe94Dea0c9BA0a6dAf8C6e196",
    "CRV":   "0x8Ee73c484A26e0A5df2Ee2a4960B789967dd0415",
    "SNX":   "0x22e6966B799c4D5B13BE962E1D117b56327FDa66",

    # =========================
    # BASE ECOSYSTEM TOKENS
    # =========================
    "DEGEN":   "0x4ed4e862860bed51a9570b96d89af5e1b0efefed",
    "BRETT":   "0x532f27101965dd16442E59d40670FaF5eBB142E4",
    "TOSHI":   "0xAC1Bd2486aAf3B5C0fc3Fd868558b082a531B2B4",
    "HIGHER":  "0x0578d8a44db98b23bf096a382e016e29a5ce0ffe",
    "MIGGLES": "0xB1a03EdA10342529bBF8EB700a06C60441fEf25d",
    "DOGINME": "0x6921B130D297cc43754afba22e5EAc0FBf8Db75b",
    "NORMIE":  "0x47b464eDB8Dc9BC67b5CD4C9310BB87b773845bD",

    # =========================
    # MEME / HIGH VOL LIQUIDITY
    # =========================
    "MOCHI":   "0xF6e932Ca12afa26665dC4dDE7e27be02A7c02e50",
    "AIDOGE":  "0xb34457736aa191ff423f84f5d669f68b231e6c4e",
    "BOB":     "0x6234641eae20d15f803441F348352794419b44c7",
    "PEPEBSC": "0x52b492a33e447cdb854c7fc19f1e57e8bfa1777d",
    "WOJAK":   "0xD512B95FC410d365181Afd9db191b078EE07A520",

    # =========================
    # ADDITIONAL LIQUID PAIRS
    # =========================
    "cbBTC": "0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf",
    "rETH":  "0xB6fe221Fe9EeF5aBa221c348bA20A1Bf5e73624c",
    

    # =========================
    # STABLE VARIANTS / BRIDGED
    # =========================
    "USDT": "0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2",
    "USDbC": "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA",

    # =========================
    # LONG TAIL LIQUIDITY (HIGH RISK BUT USEFUL FOR ARB)
    # =========================
    "1INCH": "0xc5fecc3a29fb57b5024eec8a2239d4621e111cbe",
    "SUSHI": "0x7D49a065D17d6d4a55dc13649901fdBB98B2AFBA",
    "OP":    "0x4200000000000000000000000000000000000042",

}


def get_tokens():
    return TOKENS_BASE
