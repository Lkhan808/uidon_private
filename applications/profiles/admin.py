from django.contrib import admin

from applications.profiles.models import ExecutorProfile, CustomerProfile, ProfileView

# Register your models here.
admin.site.register(ExecutorProfile)
admin.site.register(CustomerProfile)
admin.site.register(ProfileView)