from os import name, stat
from .config.coin import coin_references_all, get_coin_data

from django.db                 import models
from django.db.models.deletion import CASCADE


# Create our Member model
class Owner(models.Model):
    # Declare object attributes in our schema (define schema)
    username   = models.CharField(max_length=60)
    first_name = models.CharField(max_length=30)
    last_name  = models.CharField(max_length=30)
    email      = models.CharField(max_length=60)

    def get_absolute_url(self):
        return '/owner/list'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Portfolio(models.Model):
    coin_list  = models.CharField(max_length=15, choices=coin_references_all())
    investment = models.FloatField()
    owner      = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner.first_name} {self.owner.last_name} ({self.coin_list})"

    @property
    def balance(self):
        if not isinstance(self.coin_list, list):
            coin_list = [self.coin_list,]

        coin_list = coin_list
        
        for coin in coin_list:
            coin_df       = get_coin_data(coin)
            current_price = coin_df["price_close"][-1] if coin_df else 0.0

        return current_price
    
    def get_absolute_url(self):
        return '/portfolio/list'


class Coin(models.Model):
    start_date    = models.DateTimeField()
    price_open    = models.FloatField()
    price_high    = models.FloatField()
    price_low     = models.FloatField()
    price_close   = models.FloatField()
    volume_traded = models.FloatField()
    trades_count  = models.IntegerField()
    ticker        = models.CharField(max_length=8)
    name          = models.CharField(max_length=30)

    class Meta:
        abstract = True


class Aave(Coin):
    def __str__(self):
        return self.start_date


class Aragon(Coin):
    def __str__(self):
        return self.start_date


class Augur(Coin):
    def __str__(self):
        return self.start_date


class Balancer(Coin):
    def __str__(self):
        return self.start_date


class Bitcoin(Coin):
    def __str__(self):
        return self.start_date


class Cardano(Coin):
    def __str__(self):
        return self.start_date


class Cosmos(Coin):
    def __str__(self):
        return self.start_date


class Ethereum(Coin):
    def __str__(self):
        return self.start_date


class EthereumClassic(Coin):
    def __str__(self):
        return self.start_date


class Orchid(Coin):
    def __str__(self):
        return self.start_date


class Tether(Coin):
    def __str__(self):
        return self.start_date


class Tezos(Coin):
    def __str__(self):
        return self.start_date

