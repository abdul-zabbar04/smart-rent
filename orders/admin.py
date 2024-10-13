from django.contrib import admin
from orders.models import FavoriteModel, OrderModel

admin.site.register(FavoriteModel)
admin.site.register(OrderModel)
