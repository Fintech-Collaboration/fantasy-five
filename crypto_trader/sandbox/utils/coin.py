import os
from django.db import models

import pandas as pd

from pathlib import Path


BASE_DIR = r"C:\Users\JasonGarcia24\FINTECH\workspace\fantasy-five\crypto_trader\sandbox\data"


def icon_path(ticker):   
    return f"img/{ticker.lower()}-icon-64x64.png"


def get_coin_data(name, ticker):
    data_file = os.path.join(BASE_DIR, f"{name.lower()}_5_year.csv")

    df = pd.read_csv(
        Path(data_file),
        index_col=f"{ticker.lower()}_start_date",
        parse_dates=True,
        infer_datetime_format=True,
    )

    return df.sort_index(ascending=True)

