from django.contrib import admin

from applications.profiles.models import ExecutorProfile, CustomerProfile

# Register your models here.
admin.site.register(ExecutorProfile)
admin.site.register(CustomerProfile)