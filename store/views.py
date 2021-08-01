from pyexpat.errors import messages
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from .models import Product, Order, OrderItem
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from .cart import Cart
from .forms import CartAddProductForm, RegisterUserForm, LoginUserForm, ChangePersonalInformationForm
from .forms import OrderCreateForm


class Catalog(ListView):
    paginate_by = 6
    model = Product
    context_object_name = 'page_obj'
    template_name = 'store/catalog.html'

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.request.GET.get('type'):
            queryset = queryset.filter(type=self.request.GET.get('type'))
        if self.request.GET.get('manufacturer'):
            queryset = queryset.filter(manufacturer=self.request.GET.get('manufacturer'))
        return queryset


# def catalog(request):
#     products = Product.objects.all()
#
#     # filter
#     if "type" in request.GET:
#         products = products.filter(type__in=request.GET.getlist("type"))
#     if "manufacturer" in request.GET:
#         products = products.filter(manufacturer__title__in=request.GET.getlist("manufacturer"))
#
#     # Paginate
#
#     paginator = Paginator(products, 3)
#     # if "type" in request.GET:
#     #     page_number = request.GET.get('page', 'type')
#     # if "manufacturer" in request.GET:
#     #     page_number = request.GET.get('page', 'manufacturer')
#     # else:
#     page_number = request.GET.get('page',)
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'store/catalog.html', {'page_obj': page_obj, 'type': type, 'manufacturer': manufacturer})


class Searcher(ListView):
    paginate_by = 3
    model = Product
    context_object_name = 'page_obj'
    template_name = 'store/catalog.html'

    def get_queryset(self):
        search_params = self.request.GET['search']
        return Product.objects.filter(title__icontains=search_params)

# def search(request):
#     search_params = request.GET['search']
#     query = Product.objects.filter(title__icontains=search_params)
#     return render(request, 'store/base.html', {'query': query})

# class ShowProduct(DetailView):
#     model = Product
#     template_name = 'store/product.html'


def product(request, pk):
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

# мне нужно перестроить фунуцию таким образом,чтобы request.user присваивался атрибуту custamer модели Order
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
             OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            return render(request, 'store/order_created.html', {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'store/order_create.html', {'cart': cart, 'form': form})


# class OrderCreate(CreateView):
#     model = Order
#     fields = ['first_name', 'last_name', 'email', 'city', 'address']
#     template_name = 'store/order_create.html'
#     success_url = reverse_lazy('store:order_created')
#
#       def __init__(self):
#            if request.user.is_authenticated:
#               return Order.customer=request.user
#
#
#     def __init__(self):
#         cart = Cart(request)
#         if request.method == 'POST':
#             for item in cart:
#                 OrderItem.objects.create(order=Order, product=item['product'],
#                                          price=item['price'], quantity=item['quantity'])
#                 return redirect('store:order_created.html')
#         else:
#             pass


class OrderCreated(TemplateView):
    template_name = 'store/order_created.html'


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


# def logout_user(request):
#     logout(request)
#     return redirect('store:catalog')


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
    fields = ['last_name', 'first_name', 'email']
    template_name = 'store/change_personal_info.html'
    success_url = reverse_lazy('store:catalog')


class ShowInfo(TemplateView):
    template_name = 'store/info.html'