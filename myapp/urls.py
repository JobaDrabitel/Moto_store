from django.urls import path
from . import views
from .views import home, catalog, product_detail, cart, delivery, about, profile, add_to_cart, \
    remove_from_cart
from .views import contact, add_product, registration, user_login, user_logout, order_create, order_detail


app_name = 'myapp'

urlpatterns = [
    path('', home, name='home'),
    path('catalog/', catalog, name='catalog'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
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
    path('order_create/', views.order_create, name='order_create'),
    path('order_detail/<int:order_id>/', order_detail, name='order_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart')

]
