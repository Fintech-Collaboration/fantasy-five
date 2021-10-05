from django.db import models


class Member(models.Model):
    first_name = models.CharField(max_length=30)
    last_name  = models.CharField(max_length=30)
    phone      = models.CharField(max_length=30)

    def get_absolute_url(self):
        return '/member/list'

    def __str__(self):
        return self.first_name + " " + self.last_name

