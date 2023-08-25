from django.contrib import admin
from .models import FeedbackOnExecutor, FeedbackOnCustomer

admin.site.register(FeedbackOnExecutor)
admin.site.register(FeedbackOnCustomer)