from rest_framework import viewsets, generics
from myapp.models import User, Product
from .serializers import UserSerializer, ProductSerializer

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
