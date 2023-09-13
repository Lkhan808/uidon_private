from django.contrib import admin

from applications.qualifications.models import (
    Skill,
    Language,
    Contact,
    Portfolio
)

# Register your models here.
admin.site.register(Skill)
admin.site.register(Language)
admin.site.register(Contact)
admin.site.register(Portfolio)