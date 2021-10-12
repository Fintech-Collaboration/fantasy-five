from os import name, stat

from django.db.models.fields import BLANK_CHOICE_DASH, CharField
from .utils.coin import get_coin_data

from django.db                  import models
from django.db.models.deletion  import CASCADE

from multiselectfield import MultiSelectField
from django_userforeignkey.models.fields import UserForeignKey


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
    __ticker__ = "AAVE"
    
    def __str__(self):
        return self.start_date


class Aragon(Coin):
    __ticker__ = "ANT"
    
    
    def __str__(self):
        return self.start_date


class Augur(Coin):
    __ticker__ = "REP"
    
    def __str__(self):
        return self.start_date


class Balancer(Coin):
    __ticker__ = "BAL"
    
    def __str__(self):
        return self.start_date


class Bitcoin(Coin):
    __ticker__ = "BTC"

    def __str__(self):
        return self.start_date


class Cardano(Coin):
    __ticker__ = "ADA"
    
    def __str__(self):
        return self.start_date


class Cosmos(Coin):
    __ticker__ = "ATOM"
    
    def __str__(self):
        return self.start_date


class Ethereum(Coin):
    __ticker__ = "ETH"
    
    def __str__(self):
        return self.start_date


class EthereumClassic(Coin):
    __ticker__ = "ETC"
    
    def __str__(self):
        return self.start_date


class Orchid(Coin):
    __ticker__ = "OXT"
    
    def __str__(self):
        return self.start_date


class Tether(Coin):
    __ticker__ = "USDT"
    
    def __str__(self):
        return self.start_date


class Tezos(Coin):
    __ticker__ = "XTZ"
    
    def __str__(self):
        return self.start_date


class Portfolio(models.Model):
    choices = [(cm.__ticker__.upper(), cm.__name__) for cm in Coin.__subclasses__()]

    nickname   = CharField(max_length=20)
    coin_list  = MultiSelectField(choices=choices)
    investment = models.FloatField(default=10000)
    owner      = UserForeignKey(auto_user_add=True)

    def __str__(self):
        return f"{self.owner.first_name} {self.owner.last_name} ({self.coin_list})"

    # @property
    # def balance(self):
    #     if not isinstance(self.coin_list, list):
    #         coin_list = [self.coin_list,]

    #     coin_list = coin_list
        
    #     for coin in coin_list:
    #         coin_df       = get_coin_data(coin)
    #         current_price = coin_df["price_close"][-1] if coin_df else 0.0

    #     return current_price
    
    def get_absolute_url(self):
        return '/portfolio/list'