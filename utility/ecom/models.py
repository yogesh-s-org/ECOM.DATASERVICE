
from django.db import models
import uuid

class User(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.TextField()
	email = models.TextField()
	phone = models.TextField()
	role = models.TextField()

	def __str__(self):
		return self.name

class Address(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
	street = models.TextField()
	city = models.TextField()
	district = models.TextField()
	state = models.TextField()
	pincode = models.TextField()

	def __str__(self):
		return f"{self.street}, {self.city}"

class Product(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.TextField()
	description = models.JSONField()
	sellingPrice = models.DecimalField(max_digits=12, decimal_places=2)
	maxRetailPrice = models.DecimalField(max_digits=12, default=0, decimal_places=2)
	category = models.TextField()
	avgRating = models.FloatField(default=0.0)
	totalRatings = models.FloatField(default=0.0)
	is_available = models.BooleanField(default=True)
	stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='products')

	def __str__(self):
		return self.name

class Stock(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	quantity = models.IntegerField()
	unit = models.TextField()

	def __str__(self):
		return f"{self.product.name} - {self.quantity}"

class Image(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	url = models.TextField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

	def __str__(self):
		return self.url

class Cart(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
	quantity = models.CharField(max_length=255)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')

	def __str__(self):
		return f"Cart {self.id}"

class Wishlist(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')

	def __str__(self):
		return f"Wishlist {self.id}"

class Orders(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
	address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders')
	price = models.DecimalField(max_digits=12, decimal_places=2)
	status = models.TextField()

	def __str__(self):
		return f"Order {self.id}"


