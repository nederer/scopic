from api import models
from scopic_task.celery import app
from home_page.models import Product

from django.contrib.auth.models import User


@app.task
def check_auto_bids(product_id, user_id):
    auto_bids = models.BidsHistory.objects.filter(
        product_id=product_id,
        auto_bid=True).order_by("date")

    """
    For PostgreSQL
    users = auto_bids.exclude(user_id=user_id).distinct("users").values_list("user", flat=True)
    """

    # For Sqlite3 and MySQL
    users = auto_bids.exclude(user_id=user_id).values_list("user", flat=True)
    users = set(users)

    for user_id in users:
        outbid(user_id, product_id)


def outbid(user_id, product_id):
    product = Product.objects.get(pk=product_id)
    user = User.objects.get(pk=user_id)

    product_current_bid = product.current_bid
    if not models.UserAutoBidding.objects.get(user=user).max_bids < product_current_bid + 1:
        make_bid(product, user, product_current_bid + 1)
        subtract_bid(user, product_current_bid + 1)


def make_bid(product, user, bid_amount):
    bid = models.BidsHistory(
        user=user,
        product=product,
        bid_amount=bid_amount
    )
    bid.save()

    product.current_bid = bid_amount
    product.save()


def subtract_bid(user, bid_amount):
    user_auto_bids = models.UserAutoBidding.objects.get(user=user)
    user_auto_bids.max_bids -= bid_amount
    user_auto_bids.save()
