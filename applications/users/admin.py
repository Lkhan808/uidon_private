from django.contrib import admin
from applications.users.models import (
    User,
    CustomerProfile,
    ExecutorProfile,
    Skill,
    Review,
    Rating,
    Contact,
    Portfolio,
    Language,
    Education
)


admin.site.register(User)
admin.site.register(Contact)
admin.site.register(ExecutorProfile)
admin.site.register(CustomerProfile)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Skill)
admin.site.register(Portfolio)
admin.site.register(Education)
admin.site.register(Language)
