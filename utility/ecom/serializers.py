from rest_framework import serializers
from .models import Rating, User, Address, Product, Stock, Image, Cart, Wishlist, Orders, Category

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'street', 'city', 'district', 'state', 'pincode']

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['quantity', 'unit']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [ 'url']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rating', 'review']

class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    stock = StockSerializer(read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'selling_price', 'max_retail_price',
                 'category', 'stock', 'images', 'ratings']

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'quantity', 'product']

class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product']

class OrdersSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Orders
        fields = ['id', 'product', 'user', 'address', 'price', 'status']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']