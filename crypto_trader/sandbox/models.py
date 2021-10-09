from django.db import models


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
    coin       = models.CharField(max_length=15)
    coin_count = models.FloatField()
    owner      = models.ForeignKey(Owner, on_delete=models.CASCADE)

