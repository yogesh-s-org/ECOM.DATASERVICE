from rest_framework import serializers
from .models import User, Address, Product, Stock, Image, Cart, Wishlist, Orders, Category

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'street', 'city', 'district', 'state', 'pincode']

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'quantity', 'unit']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'url', 'product']

class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    stock = StockSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'sellingPrice', 'maxRetailPrice', 
                 'category', 'avgRating', 'totalRatings', 'is_available', 
                 'stock', 'images']

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

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    orders = OrdersSerializer(many=True, read_only=True)
    wishlists = WishlistSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'role', 'addresses', 
                 'orders', 'wishlists']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']