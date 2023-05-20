from decimal import Decimal

import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from requests import request
from unicodedata import decimal

from myapp.models import Product, PaymentMethod
from .forms import OrderForm
from .forms import RegistrationForm
from .forms import UserProfileForm
from .models import Order, OrderItem, ShippingMethod, OrderDelivery
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', [])
    try:
        item_id = int(item_id)  # Преобразование в целочисленное значение
        if item_id in cart:
            cart.remove(item_id)
            request.session['cart'] = cart
        return redirect('myapp:cart')
    except (ValueError, KeyError):
        # Обработка случая, когда item_id не является числом или предмет не найден в корзине
        return HttpResponse('Item not found in cart.')






def cart(request):
    cart_products_ids = request.session.get('cart', [])
    cart_products = Product.objects.filter(id__in=cart_products_ids)
    cart_total_price = cart_products.aggregate(total_price=Sum('price'))['total_price'] or 0

    context = {
        'cart_products': cart_products,
        'cart_total_price': cart_total_price,
    }
    return render(request, 'cart.html', context)



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # Проверяем, есть ли уже корзина в сессии
    if 'cart' not in request.session:
        request.session['cart'] = []

    # Добавляем товар в корзину в сессии
    request.session['cart'].append(product.id)
    request.session.modified = True  # Сохраняем изменения в сессии

    return redirect('myapp:cart')



def get_random_question():
    response = requests.get('http://jservice.io/api/random')
    if response.status_code == 200:
        data = response.json()
        if data:
            question = data[0]['question']
            answer = data[0]['answer']
            print (answer)
            return question, answer
    return None, None
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_delivery = OrderDelivery.objects.get(order=order)

    context = {
        'order': order,
        'order_delivery': order_delivery,
    }
    return render(request, 'order_detail.html', context)



@transaction.atomic
def order_create(request):
    shipping_methods = ShippingMethod.objects.all()
    payment_methods = PaymentMethod.objects.all()

    cart_products_ids = request.session.get('cart', [])
    cart_products = Product.objects.filter(id__in=cart_products_ids)

    total_price = sum(product.price for product in cart_products)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            user = request.user
            print('valid')
            with transaction.atomic():
                user_answer = request.POST.get('answer')
                correct_answer = request.session['question']['answer']
                if user_answer == correct_answer:
                    total_price -= total_price * Decimal('0.05')
                order = Order.objects.create(user=user, total_price=total_price)
                async_to_sync(channel_layer.group_send)(
                    "notifications",
                    {"type": "notify_new_order", "order_id": order.id}
                )
                for product in cart_products:
                    quantity = request.session['cart'].count(product.id)
                    price = product.price

                OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

                shipping_method_id = request.POST.get('shipping_method')
                if shipping_method_id is not None:
                    shipping_method = get_object_or_404(ShippingMethod, pk=shipping_method_id)
                payment_method_id = form.cleaned_data['payment_method'].id
                address = form.cleaned_data['address']
                payment_method = PaymentMethod.objects.get(pk=payment_method_id)
                order_delivery = OrderDelivery.objects.create(
                    order=order, shipping_method=shipping_method, payment_method=payment_method, address=address
                )

                request.session['cart'] = []

            return redirect('myapp:order_detail', order_id=order.id)
        else:
            print('Form is not valid')
    else:
        form = OrderForm()

    question, answer = get_random_question()
    request.session['question'] = {'question': question, 'answer': answer}

    context = {
        'form': form,
        'shipping_methods': shipping_methods,
        'payment_methods': payment_methods,
        'cart_products': cart_products,
        'total_price': total_price,
        'question': question,
        'answer': answer,
    }
    return render(request, 'order_create.html', context)





    context = {
        'form': form,
        'product': product,
        'shipping_methods': shipping_methods,
        'payment_methods': payment_methods,
        'product_id': product_id,
        'question': question
    }
    return render(request, 'order_detail.html', {'order': order})




def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'profile.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def home(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'home.html', context)


def catalog(request):
    products = Product.objects.order_by('-id')  # Получить все записи, упорядоченные по убыванию идентификаторов
    context = {
        'products': products
    }
    return render(request, 'catalog.html', context)





def favorites(request):
    # Получение избранных товаров пользователя
    # Отображение избранных товаров

    return render(request, 'favorites.html')



def delivery(request):
    shipping_methods = ShippingMethod.objects.all()
    context = {
        'shipping_methods': shipping_methods
    }
    return render(request, 'delivery.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


@staff_member_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        imageurl = request.POST.get('imageurl')

        product = Product(
            name=name,
            category=category,
            description=description,
            price=price,
            imageurl=imageurl
        )
        product.save()

        return redirect('catalog')
    else:
        return render(request, 'add_product.html')