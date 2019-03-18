from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.crypto import get_random_string
import hashlib


# Create your models here.
class Admin(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.user.username

class Category(models.Model):
	name = models.CharField(max_length = 200)

	def __str__(self):
		return self.name

class Location(models.Model):
	name = models.CharField(max_length = 200)

	def __str__(self):
		return self.name

class Client(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	address = models.CharField(max_length = 200, null = True)
	phone = models.CharField(max_length = 200, null = True)
	website = models.CharField(max_length = 200, null = True)
	fb = models.CharField(max_length = 200, null = True)
	verified = models.BooleanField(default = False)

	def __str__(self):
		return self.user.username

class Ad(models.Model):
	title = models.CharField(max_length = 200)
	description = models.CharField(max_length = 500, null = True)
	services = models.CharField(max_length = 500, null = True)
	image = models.ImageField(upload_to = 'media/')
	date  = models.DateTimeField(null=False,blank=True,default=datetime.now())
	verified = models.BooleanField(default = False)
	client = models.ForeignKey(Client, on_delete = models.CASCADE)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	location = models.ForeignKey(Location, on_delete = models.CASCADE)

	def __str__(self):
		return self.title + " - " + str(self.client)

class Activation(models.Model):
    profile_ref = models.OneToOneField(Client, on_delete = models.CASCADE)
    activation_code = models.CharField(max_length = 50)
    expiry = models.DateField(auto_now_add=False)
    def getActivationCode(self, username):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(20, chars)
        return hashlib.sha256((secret_key + username).encode('utf-8')).hexdigest()

class Event(models.Model):
	client = models.ForeignKey(Client, on_delete = models.CASCADE, null = True)
	title = models.CharField(max_length = 200)
	description = models.CharField(max_length = 200)
	time = models.DateTimeField(default = datetime.now())
	venue = models.CharField(max_length = 200)
	fees = models.TextField()
	location = models.ForeignKey(Location, on_delete = models.CASCADE)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	verified = models.BooleanField(default = False)
	image = models.ImageField(upload_to = 'media/', null = True)

	def __str__(self):
		return self.title

class Advertisement(models.Model):
	image = models.ImageField(upload_to = 'media/')
