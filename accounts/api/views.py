from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.response import Response

from products.models import Product

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny, ))
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username is None or password is None:
        return Response({'error': 'Please provide both credentials'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalive Credentials'}, status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'username': user.username, 'token': token.key, 'email': user.email, 'id': user.id},
            status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny, ))
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    if username is None or email is None or password is None:
        return Response({'error': 'Please provide the required credentials'}, status=HTTP_400_BAD_REQUEST)
    new_user = get_user_model().objects.create(username=username, password=password, email=email)
    token = Token.objects.create(user=new_user)
    return Response({'username': new_user.username, 'token': token.key, 'email': new_user.email, 'id': new_user.id},
        status=HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def add_to_cart(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    user.cart.add(product)
    products = user.cart.values_list('id', flat=True)
    return Response({'products': products}, status=HTTP_200_OK)

@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def remove_from_cart(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    user.cart.remove(product)
    products = user.cart.values_list('id', flat=True)
    return Response({'products': products}, status=HTTP_200_OK)

@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def cart(request):
    user = request.user
    products = user.cart.values_list('id', flat=True)
    return Response({'products': products}, status=HTTP_200_OK)