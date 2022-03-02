from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'products-api'

router = routers.DefaultRouter()
router.register(r'categories', views.CategorieViewSet)
router.register(r'', views.ProductViewSet)


urlpatterns = [
	path('', include(router.urls)),
]