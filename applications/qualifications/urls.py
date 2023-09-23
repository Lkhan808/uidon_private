from django.urls import path
from . import views

urlpatterns = [
    path('skills/', views.skill_list_create_view),
    path('skills/<int:pk>/', views.skill_detail_view),

    path('languages/', views.language_list_create_view),
    path('languages/update-or-delete/', views.language_detail_view),

    path('contacts/', views.contact_list_create_view),
    path('contacts/update-or-delete/', views.contact_detail_view),

    path('portfolios/', views.portfolio_list_create_view),
    path('portfolios/update-or-delete/', views.portfolio_detail_view),
]