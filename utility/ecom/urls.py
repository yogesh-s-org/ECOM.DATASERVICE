from django.urls import path
from .views import get_products, get_categories

urlpatterns = [
    path('products/', get_products, name='get_products'),
    path('categories/', get_categories, name='get_categories'),
]