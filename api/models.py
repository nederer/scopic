from django.db import models
from django.contrib.auth.models import User

from home_page.models import Product


class BidsHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    bid_amount = models.IntegerField()
    auto_bid = models.BooleanField(default=False)


class UserAutoBidding(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    max_bids = models.IntegerField(default=150)
