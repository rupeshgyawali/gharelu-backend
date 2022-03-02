from django.urls import path

from accounts.api import views

app_name = "accounts-api"

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart, name="cart"),
    path('cart/add/<int:pk>/', views.add_to_cart, name="add_to_cart"),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name="remove_from_cart"),
]