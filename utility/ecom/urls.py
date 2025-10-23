from django.urls import path
from .views import get_products, get_categories, get_product_detail, register, login

urlpatterns = [
    path('sign-up/', register, name='register'),
    path('sign-in/', login, name='login'),
    path('products/', get_products, name='get_products'),
    path('categories/', get_categories, name='get_categories'),
    path('products/<uuid:product_id>/', get_product_detail, name='get_product_detail'),
]