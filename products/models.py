from django.conf import settings
from django.db import models

def upload_image(instance, filename):
    return f"products/{instance.id}/{filename}"

class Product(models.Model):
    vender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    price = models.IntegerField()
    details = models.TextField()
    image = models.ImageField(upload_to=upload_image, null=True, blank=True)

    def __str__(self):
        return self.name


class Categorie(models.Model):
    name = models.CharField(max_length = 250)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name
    