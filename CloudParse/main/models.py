from django.db import models

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=200, primary_key=True)
	email = models.CharField(max_length=200)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	image = models.CharField(max_length=200)
	password_hash = models.CharField(max_length=200)
	salt = models.CharField(max_length=200)
	last_login = models.DateTimeField('last logged in')

class Comment(models.Model):
	user = models.ForeignKey(User)
	