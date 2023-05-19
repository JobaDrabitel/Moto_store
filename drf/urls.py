from django.urls import include, path
from rest_framework import routers
from .views import UserListAPIView, ProductListAPIView

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),

]
