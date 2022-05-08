from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
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
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        elif self.request.GET.get('type'):
            types = self.request.GET.getlist('type')
            queryset = queryset.filter(type__in=types)
        elif self.request.GET.get('manufacturer'):
            manufacturers = self.request.GET.getlist('manufacturer')
            queryset = queryset.filter(manufacturer__in=manufacturers)
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
    template_name = 'store/change_password.html'
    form_class = ChangePasswordForm


def show_personal_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'store/personal_order.html', {'order': order})
