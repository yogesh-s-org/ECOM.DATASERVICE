from django.urls import path
from .views import get_products, get_categories, get_product_detail, register, login, add_product_to_wishlist, get_wishlist
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('sign-up/', register, name='register'),
    path('sign-in/', login, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/', get_products, name='get_products'),
    path('categories/', get_categories, name='get_categories'),
    path('products/<uuid:product_id>/', get_product_detail, name='get_product_detail'),
    path('add-to-wishlist/', add_product_to_wishlist, name='add_product_to_wishlist'),
    path('wishlist/', get_wishlist, name='get_wishlist'),
]