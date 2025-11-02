
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
import random
import string

class User(AbstractUser):
    # Set unique=True to ensure one phone per account
    email = models.EmailField(unique=True)
    username = None 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
	    return self.email

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    # OTP is valid for 5 minutes
    expiry_time = models.DateTimeField(null=True, blank=True) 

    def is_valid(self):
        """Checks if the OTP has expired."""
        return timezone.now() < self.expiry_time
    
    @staticmethod
    def generate_code():
        """Generates a random 6-digit numeric OTP."""
        return ''.join(random.choices(string.digits, k=6))

    def save(self, *args, **kwargs):
        # Set expiry time 5 minutes from now if not already set
        if not self.pk: 
            self.expiry_time = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.phone_number} - {self.otp_code}"

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
	subtitle = models.CharField(max_length=255, null=True, blank=True)
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


