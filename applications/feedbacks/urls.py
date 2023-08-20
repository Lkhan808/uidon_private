from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.review_list_create_view, name='review-list-create'),
    path('reviews/<int:pk>/', views.review_detail_view, name='review-detail'),

    path('ratings/', views.rating_list_create_view, name='rating-list-create'),
    path('ratings/<int:pk>/', views.rating_detail_view, name='rating-detail'),
]
