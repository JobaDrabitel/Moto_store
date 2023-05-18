from django.urls import path
from . import views
from .views import home, catalog, product_detail, order, favorites, cart, delivery, about, profile
from .views import contact, add_product, registration, user_login, user_logout, order_create


app_name = 'myapp'

urlpatterns = [
    path('', home, name='home'),
    path('catalog/', catalog, name='catalog'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('order/', order, name='order'),
    path('favorites/', favorites, name='favorites'),
    path('cart/', cart, name='cart'),
    path('delivery/', delivery, name='delivery'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('add-product/', add_product, name='add_product'),
    path('registration/', registration, name='registration'),
    path('user_login/', user_login, name='user_login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('catalog/product/<int:product_id>/', product_detail, name='product_detail'),
    path('catalog/product/<int:product_id>/', product_detail, name='product_detail'),
    path('order_create/<int:product_id>/', order_create, name='order_create'),
]
