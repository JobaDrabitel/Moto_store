from myapp.models import Product, Cart, Order, User, OrderItem, ShippingMethod, PaymentMethod, OrderDelivery
from django.contrib.admin.views.decorators import staff_member_required
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.shortcuts import render, get_object_or_404
from myapp.models import Product
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem, ShippingMethod, PaymentMethod
from django.shortcuts import render, get_object_or_404
from .models import Product, Order
from django.shortcuts import render, redirect
from myapp.forms import OrderForm
from myapp.models import Product, Order, OrderItem, ShippingMethod, PaymentMethod


def order_create(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            # Получите выбранный способ доставки и оплаты из формы
            # и сохраните их соответствующие объекты моделей ShippingMethod и PaymentMethod

            # Создайте заказ
            order = Order.objects.create(user=request.user, total_price=product.price)

            # Создайте элемент заказа для выбранного товара
            order_item = OrderItem.objects.create(order=order, product=product, quantity=1, price=product.price)

            # Создайте объект OrderDelivery для заказа
            # Передайте в него объекты ShippingMethod, PaymentMethod, и другие данные о доставке

            # Сохраните заказ и связанные объекты
            order.save()
            order_item.save()
            # Сохраните OrderDelivery

            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()

    context = {'form': form, 'product': product}
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


