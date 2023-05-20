from rest_framework import viewsets, generics
from myapp.models import User, Product
from .serializers import UserSerializer, ProductSerializer
from django.urls import reverse
from myapp.models import Product
from drf.serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': request.build_absolute_uri(reverse('user-list')),
        'products': request.build_absolute_uri(reverse('product-list')),
    })
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer