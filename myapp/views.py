import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from requests import request
from myapp.models import Product, PaymentMethod
from .forms import OrderForm
from .forms import RegistrationForm
from .forms import UserProfileForm
from .models import Order, OrderItem, ShippingMethod, OrderDelivery
from django.shortcuts import get_object_or_404

def get_random_question():
    response = requests.get('http://jservice.io/api/random')
    if response.status_code == 200:
        data = response.json()
        if data:
            question = data[0]['question']
            answer = data[0]['answer']
            return question, answer
    return None, None
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_detail.html', {'order': order})


@transaction.atomic
def order_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    shipping_methods = ShippingMethod.objects.all()
    payment_methods = PaymentMethod.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Получаем ответ пользователя из формы
            user_answer = form.cleaned_data['answer']
            # Получаем сохраненное значение вопроса из сеанса
            question = request.session.get('question')
            # Проверяем ответ пользователя
            if question and question['answer'] == user_answer:
                total_price = float(product.price) * float(0.95)
                print('good')
            else:
                total_price = product.price
                print('no')
            order = Order.objects.create(user=request.user, total_price=total_price)
            order_item = OrderItem.objects.create(order=order, product=product, quantity=1, price=product.price)
            shipping_method_id = form.cleaned_data['shipping_method']
            payment_method_id = form.cleaned_data['payment_method']
            address = form.cleaned_data['address']
            shipping_method = get_object_or_404(ShippingMethod, pk=shipping_method_id.id)
            payment_method = get_object_or_404(PaymentMethod, pk=payment_method_id.id)
            order_delivery = OrderDelivery.objects.create(order=order, shipping_method=shipping_method,
                                                          payment_method=payment_method, address=address)

            return redirect('myapp:order_detail', order_id=order.id)
        else:
            print('Пошел нахуй')
    else:
        form = OrderForm()

    question, answer = get_random_question()
    print(answer)
    request.session['question'] = {'question': question, 'answer': answer}

    context = {
        'form': form,
        'product': product,
        'shipping_methods': shipping_methods,
        'payment_methods': payment_methods,
        'product_id': product_id,
        'question': question
    }
    return render(request, 'order_create.html', context)




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


def order(request):
    # Обработка оформления заказа
    if request.method == 'POST':
        # Получение данных из формы
        # Создание объектов Order, OrderItem и OrderDelivery
        # Сохранение объектов в базу данных

        return render(request, 'order_confirmation.html')

    return render(request, 'order.html')


def favorites(request):
    # Получение избранных товаров пользователя
    # Отображение избранных товаров

    return render(request, 'favorites.html')


def cart(request):
    # Получение корзины пользователя
    # Отображение корзины

    return render(request, 'cart.html')


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