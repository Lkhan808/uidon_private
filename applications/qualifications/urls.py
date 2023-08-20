from django.urls import path
from . import views

urlpatterns = [
    path('skills/', views.skill_list_create_view, name='skill-list-create'),
    path('skills/<int:pk>/', views.skill_detail_view, name='skill-detail'),

    path('languages/', views.language_list_create_view, name='language-list-create'),
    path('languages/<int:pk>/', views.language_detail_view, name='language-detail'),

    path('educations/', views.education_list_create_view, name='education-list-create'),
    path('educations/<int:pk>/', views.education_detail_view, name='education-detail'),

    path('contacts/', views.contact_list_create_view, name='contact-list-create'),
    path('contacts/<int:pk>/', views.contact_detail_view, name='contact-detail'),

    path('portfolios/', views.portfolio_list_create_view, name='portfolio-list-create'),
    path('portfolios/<int:pk>/', views.portfolio_detail_view, name='portfolio-detail'),
]