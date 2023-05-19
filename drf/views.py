from rest_framework import viewsets, generics
from myapp.models import User, Product
from .serializers import UserSerializer, ProductSerializer

from rest_framework import viewsets
from myapp.models import Product
from drf.serializers import ProductSerializer

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
from django.shortcuts import render
from .motorcycle_data_api import get_motorcycles

def motorcycle_search(request):
    make = request.GET.get('make')
    model = request.GET.get('model')
    motorcycles = get_motorcycles(make, model)

    context = {
        'motorcycles': motorcycles
    }
    return render(request, 'search.html', context)
