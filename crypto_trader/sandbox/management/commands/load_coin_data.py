import os

from csv      import DictReader
from datetime import datetime
from pytz     import UTC
from pathlib  import Path

from django.core.management import BaseCommand

from sandbox.models import (
    Aave,
    Aragon,
    Augur,
    Balancer,
    Bitcoin,
    Cardano,
    Cosmos,
    Ethereum,
    EthereumClassic,
    Orchid,
    Tether,
    Tezos,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

MODELS = (
    Aave,
    Aragon,
    Augur,
    Balancer,
    Bitcoin,
    Cardano,
    Cosmos,
    Ethereum,
    EthereumClassic,
    Orchid,
    Tether,
    Tezos,
)

class Command(BaseCommand):
    def handle(self, *args, **options):
        for model in MODELS:
            name = model.__name__
            file = os.path.join(BASE_DIR, "data", f"{name.lower()}_5_year.csv")

            if model.objects.exists():
                print(f"{name.capitalize()} data already loaded. Continuing...")
                continue
            
            print(f"Creating {name} data")

            for row in DictReader(open(file)):
                date_col = [x for x in row.keys() if "start_date" in x][0]
                ticker   = date_col.split("_")[0]

                coin = model()

                coin.price_open    = row["price_open"]
                coin.price_high    = row["price_high"]
                coin.price_low     = row["price_low"]
                coin.price_close   = row["price_close"]
                coin.volume_traded = row["volume_traded"]
                coin.trades_count  = row["trades_count"]
                coin.ticker        = ticker
                coin.name          = name if name.lower() != "ethereumclassic" else "ethereum classic"

                start_date         = row[date_col]
                coin.start_date = UTC.localize(
                    datetime.strptime(start_date[:-2], DATETIME_FORMAT)
                )
                
                coin.save()
            
