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
    "BAL":   "0x...BAL_BASE_ADDRESS...",
    "UNI":   "0x...UNI_BASE_ADDRESS...",
    "LINK":  "0x...LINK_BASE_ADDRESS...",
    "LDO":   "0x...LDO_BASE_ADDRESS...",
    "CRV":   "0x...CRV_BASE_ADDRESS...",
    "SNX":   "0x...SNX_BASE_ADDRESS...",

    # =========================
    # BASE ECOSYSTEM TOKENS
    # =========================
    "DEGEN":   "0x...DEGEN_ADDRESS...",
    "BRETT":   "0x...BRETT_ADDRESS...",
    "TOSHI":   "0x...TOSHI_ADDRESS...",
    "HIGHER":  "0x...HIGHER_ADDRESS...",
    "MIGGLES": "0x...MIGGLES_ADDRESS...",
    "BASEDAI": "0x...BASEDAI_ADDRESS...",
    "DOGINME": "0x...DOGINME_ADDRESS...",
    "NORMIE":  "0x...NORMIE_ADDRESS...",

    # =========================
    # MEME / HIGH VOL LIQUIDITY
    # =========================
    "MOCHI":   "0x...MOCHI_ADDRESS...",
    "AIDOGE":  "0x...AIDOGE_ADDRESS...",
    "BOB":     "0x...BOB_ADDRESS...",
    "BISO":    "0x...BISO_ADDRESS...",
    "PEPEBSC": "0x...PEPE_LIKE_BASE...",
    "WOJAK":   "0x...WOJAK_BASE...",

    # =========================
    # ADDITIONAL LIQUID PAIRS
    # =========================
    "cbBTC": "0x...CBBTC_ADDRESS...",
    "WBTC":  "0x...WBTC_BASE_ADDRESS...",
    "rETH":  "0x...RETH_ADDRESS...",
    "stETH": "0x...STETH_WRAPPED_BASE...",

    # =========================
    # STABLE VARIANTS / BRIDGED
    # =========================
    "USDT": "0x...USDT_BASE_ADDRESS...",
    "USDC.e": "0x...USDC_BRIDGED_ADDRESS...",

    # =========================
    # LONG TAIL LIQUIDITY (HIGH RISK BUT USEFUL FOR ARB)
    # =========================
    "MAGIC": "0x...MAGIC_ADDRESS...",
    "GRT":   "0x...GRT_ADDRESS...",
    "1INCH": "0x...1INCH_ADDRESS...",
    "SUSHI": "0x...SUSHI_ADDRESS...",
    "OP":    "0x4200000000000000000000000000000000000042",

}


def get_tokens():
    return TOKENS_BASE
