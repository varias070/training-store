from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from .models import Product, OrderItem, Type, Manufacturer
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import *


class Catalog(ListView):
    paginate_by = 12
    model = Product
    context_object_name = 'products'
    template_name = 'store/catalog.html'

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.request.GET.get('search'):
            queryset = queryset.filter(title__icontains=self.request.GET.get('search'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(type=self.request.GET.get('type'))
        if self.request.GET.get('manufacturer'):
            queryset = queryset.filter(manufacturer=self.request.GET.get('manufacturer'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all()
        context['manufacturers'] = Manufacturer.objects.all()
        return context


def show_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_product_form = CartAddProductForm()
    return render(request, 'store/product.html', {'product': product, 'cart_product_form': cart_product_form})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'])
    return redirect('store:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('store:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.instance
            if request.user.is_authenticated:
                user = request.user
            else:
                user = User.objects.create_user(
                    email=form.cleaned_data['email'],
                    last_name=form.cleaned_data['last_name'],
                    first_name=form.cleaned_data['first_name'],
                    username=form.cleaned_data['first_name']+form.cleaned_data['last_name'],
                    password='123'
                )
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
            return render(request, 'store/order_created.html', {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'store/order_create.html', {'cart': cart, 'form': form})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'store/register.html'
    success_url = reverse_lazy('store:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('store:catalog')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'store/login.html'

    def get_success_url(self):
        return reverse_lazy('store:catalog')


class LogoutUser(LogoutView):
    next_page = 'store:catalog'


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not Found</h1>')


class ShowPersonalCabinet(DetailView):
    model = User
    template_name = 'store/personal_cabinet.html'


# def change_personal_information(request, pk):
#         user = User.objects.get(pk=pk)
#
#         if request.method == "POST":
#             user. first_name = request.POST.get('first_name')
#             user.last_name = request.POST.get('last_name')
#             user.email = request.POST.get('email')
#             user.save()
#             return redirect('store:personal_cabinet')
#         else:
#             return render(request, "change_personal_info.html", {"user": user})


class ChangePersonalInformation(UpdateView):
    model = User
    form_class = ChangePersonalInformationForm
    template_name = 'store/change_personal_info.html'
    success_url = reverse_lazy('store:catalog')


class ShowInfo(TemplateView):
    template_name = 'store/info.html'


class ChangePassword(PasswordChangeView):
    template_name = 'store/change_password.html'  # 'registration/password_change_form.html'
    form_class = ChangePasswordForm


def show_personal_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    # order_item = get_object_or_404(OrderItem, pk=pk)
    return render(request, 'store/personal_order.html', {'order': order})  # 'order_item': order_item})
