
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
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address_user')
	street = models.TextField()
	city = models.TextField()
	district = models.TextField()
	state = models.TextField()
	pincode = models.TextField()

	def __str__(self):
		return f"{self.street}, {self.city}"

class Category(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.TextField()
	description = models.TextField()

	def __str__(self):
		return self.name

class Product(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.TextField()
	description = models.JSONField()
	sellingPrice = models.DecimalField(max_digits=12, decimal_places=2)
	maxRetailPrice = models.DecimalField(max_digits=12, default=0, decimal_places=2)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
	stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='product_stock')

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
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images_product')

	def __str__(self):
		return self.url

class Rating(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_user')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings_product')
	rating = models.FloatField()
	review = models.TextField()

	def __str__(self):
		return f"Rating {self.rating} for {self.product.name}"

class Cart(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_users')
	quantity = models.CharField(max_length=255)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product')

	def __str__(self):
		return f"Cart {self.id}"

class Wishlist(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_user')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_product')

	def __str__(self):
		return f"Wishlist {self.id}"

class Orders(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders_product')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_user')
	address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders_address')
	price = models.DecimalField(max_digits=12, decimal_places=2)
	status = models.TextField()

	def __str__(self):
		return f"Order {self.id}"


