from django.contrib import admin
from .models import User, Address, Category, Product, Stock, Image, Cart, Wishlist, Orders

# Register your models here.
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(Image)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Orders)
