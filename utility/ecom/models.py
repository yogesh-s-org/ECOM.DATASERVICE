
from django.db import models
import uuid
from django.contrib.auth.models import User

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

class Category(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.name

class Stock(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	quantity = models.IntegerField()
	unit = models.CharField(max_length=40, choices=[
		('pieces', 'pieces'),
		('kg', 'kg'),
		('liters', 'liters'),
		('packs', 'packs'),
		('dozens', 'dozens')
	], default='kg')
 
	def __str__(self):
		return f"{self.quantity} / {self.unit}"

class Product(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255)
	description = models.JSONField(null=True, blank=True)
	selling_price = models.DecimalField(max_digits=12, decimal_places=2)
	max_retail_price = models.DecimalField(max_digits=12, default=0, decimal_places=2)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
	stock = models.OneToOneField(Stock, on_delete=models.CASCADE, related_name='product')

	def __str__(self):
		return self.name

class Image(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	url = models.TextField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

	def __str__(self):
		return self.url

class Rating(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
	rating = models.FloatField()
	review = models.TextField()

	def __str__(self):
		return self.review

class Cart(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
	quantity = models.IntegerField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product')

	def __str__(self):
		return self.id

class Wishlist(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist')

	def __str__(self):
		return self.id

class Orders(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
	address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders')
	price = models.DecimalField(max_digits=12, decimal_places=2)
	status = models.CharField(max_length=20, choices=[
		('pending', 'Pending'),
		('shipped', 'Shipped'),
		('delivered', 'Delivered'),
		('cancelled', 'Cancelled')
	], default='pending')

	def __str__(self):
		return self.id


