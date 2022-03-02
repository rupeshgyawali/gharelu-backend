from rest_framework import viewsets
from products.models import Product, Categorie
from products.api.serializers import ProductSerializer, CategorieSerializer


class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

class CategorieViewSet(viewsets.ModelViewSet):
	queryset = Categorie.objects.all()
	serializer_class = CategorieSerializer