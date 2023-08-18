from django.contrib import admin
from .models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Ordering)
class OrderingAdmin(admin.ModelAdmin):
    pass