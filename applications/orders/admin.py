from django.contrib import admin
from .models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderResponse)
class OrderingAdmin(admin.ModelAdmin):
    pass

@admin.register(FavoriteOrder)
class FavoriteOrderAdmin(admin.ModelAdmin):
    pass
