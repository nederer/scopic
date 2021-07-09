from django.contrib import admin
from home_page.models import Product
from api.models import BidsHistory, UserAutoBidding

admin.site.register(Product)
admin.site.register(BidsHistory)
admin.site.register(UserAutoBidding)
