from django.db import models
from django.utils import timezone

from datetime import timedelta


def set_close_date():
    now = timezone.now()
    return now + timedelta(days=3)


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    current_bid = models.IntegerField(default=15)
    close_date = models.DateTimeField(default=set_close_date)