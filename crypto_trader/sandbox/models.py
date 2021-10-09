from .config.coin import coin_references_all

from django.db import models
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


class Coin(models.Model):
    ticker        = models.CharField(max_length=15)
    name          = models.FloatField()
    current_price = models.FloatField()
    high24        = models.FloatField()
    low24         = models.FloatField()
    volume        = models.FloatField()
    market_cap    = models.FloatField()
    supply        = models.IntegerField()


class Portfolio(models.Model):
    coin_list  = models.CharField(max_length=15, choices=coin_references_all())
    investment = models.FloatField()
    balance    = models.FloatField()
    owner      = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return '/portfolio/list'

    def __str__(self):
        return f"{self.owner.first_name} {self.owner.last_name} ({self.coin_list})"

