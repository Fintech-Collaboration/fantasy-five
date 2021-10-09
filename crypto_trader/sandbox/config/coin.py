COIN_DICT = {
        "AAVE": {"name": "Aave"},
        "ADA":  {"name": "Cardano"},
        "ANT":  {"name": "Aragon"},
        "ATOM": {"name": "Cosmos"},
        "BAL":  {"name": "Balancer"},
        "BTC":  {"name": "Bitcoin"},
        "CQT":  {"name": "Covalent"},
        "ETC":  {"name": "Ethereum Classic"},
        "ETH":  {"name": "Ethereum"},
        "KAR":  {"name": "Karura"},
        "USDT": {"name": "Tether"},
        "XRP":  {"name": "Ripple"}
    }

def coin_references_all():
    return [(key, val["name"]) for key, val in COIN_DICT.items()]


def coin_references(ticker):
    return COIN_DICT[ticker]["name"]


def icon_path(ticker):   
    return f"img/{ticker.lower()}-icon-64x64.png"