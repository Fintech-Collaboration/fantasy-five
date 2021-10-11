import os

import pandas as pd

from pathlib import Path


BASE_DIR = r"C:\Users\JasonGarcia24\FINTECH\workspace\fantasy-five\crypto_trader\sandbox\data\archive"

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


def get_coin_data(ticker):
    print(ticker)
    if not ticker in COIN_DICT.keys():
        return False

    data_file = os.path.join(BASE_DIR, f"{coin_references(ticker)}_5_year.csv")

    df = pd.read_csv(
        Path(data_file),
        index_col=f"{ticker.lower()}_start_date",
        parse_dates=True,
        infer_datetime_format=True,
    )

    return df.sort_index(ascending=True)

