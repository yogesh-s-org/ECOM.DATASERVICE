from django.contrib import admin
from .models import Category, Product, Stock, Image

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'selling_price']
    inlines = []

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

ProductAdmin.inlines = [ImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Stock)