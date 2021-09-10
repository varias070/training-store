from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render
from order.forms import OrderCreateForm
from order.models import OrderItem
from registration.views import send_activation_email
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            order = form.instance
            if request.user.is_authenticated:
                user = request.user
            elif User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                login(request, user)

            else:
                user = User.objects.create_user(
                    email=form.cleaned_data['email'],
                    # last_name=form.cleaned_data['last_name'],
                    # first_name=form.cleaned_data['first_name'],
                    username=form.cleaned_data['email'],
                    password='123',
                    is_active=False,
                )
                send_activation_email(user, request)
            order.customer = user
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            return render(request, 'order_created.html', {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'order_create.html', {'cart': cart, 'form': form})
