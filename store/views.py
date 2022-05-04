from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from .models import Product, Type, Manufacturer
from django.shortcuts import render, get_object_or_404
from .forms import *
from order.models import Order


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
