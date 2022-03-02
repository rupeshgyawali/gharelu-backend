from django.contrib.auth.models import AbstractUser
from django.db import models

from products.models import Product

# Create your models here.
class User(AbstractUser):
    cart = models.ManyToManyField(Product)




