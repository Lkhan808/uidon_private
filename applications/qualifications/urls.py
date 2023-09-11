from django.urls import path
from . import views

urlpatterns = [
    path('skills/', views.skill_list_create_view),
    path('skills/<int:pk>/', views.skill_detail_view),

    path('languages/', views.language_list_create_view),
    path('languages/<int:pk>/', views.language_detail_view),

    path('contacts/', views.contact_list_create_view),
    path('contacts/<int:pk>/', views.contact_detail_view),

    path('portfolios/', views.portfolio_list_create_view),
    path('portfolios/<int:pk>/', views.portfolio_detail_view),
]