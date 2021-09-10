from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from django_registration.backends.activation.views import RegistrationView, REGISTRATION_SALT
from django_registration.exceptions import ActivationError
from .models import Product, OrderItem, Type, Manufacturer
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import *
from django.conf import settings


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
            return render(request, 'store/order_created.html', {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'store/order_create.html', {'cart': cart, 'form': form})


def create_activation_key(user):
    return signing.dumps(obj=user.get_username(), salt=REGISTRATION_SALT)


def send_activation_email(user, request):
    email_body_template = "django_registration/activation_email_body.txt"
    email_subject_template = "django_registration/activation_email_subject.txt"
    activation_key = create_activation_key(user)
    context = get_email_context(request, activation_key)
    context["user"] = user
    subject = render_to_string(
        context=context,
        template_name=email_subject_template,
        request=request,
    )
    subject = "".join(subject.splitlines())
    message = render_to_string(
        template_name=email_body_template,
        context=context,
        request=request,
    )
    user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


def get_email_context(request, activation_key):
    scheme = "https" if request.is_secure() else "http"
    return {
        "scheme": scheme,
        "activation_key": activation_key,
        "expiration_days": settings.ACCOUNT_ACTIVATION_DAYS,
        "site": get_current_site(request),
        }


def activate_user(*args, **kwargs):
    username = validate_key(kwargs.get("activation_key"))
    user = get_user(username)
    user.is_active = True
    user.save()
    return user


def validate_key(activation_key):
    ALREADY_ACTIVATED_MESSAGE = (
        "The account you tried to activate has already been activated."
    )
    BAD_USERNAME_MESSAGE = (
        "The account you attempted to activate is invalid.")
    EXPIRED_MESSAGE =(
        "This account has expired.")
    INVALID_KEY_MESSAGE = (
        "The activation key you provided is invalid.")
    try:
        username = signing.loads(
            activation_key,
            salt=REGISTRATION_SALT,
            max_age=settings.ACCOUNT_ACTIVATION_DAYS * 86400,
        )
        return username
    except signing.SignatureExpired:
        raise ActivationError(EXPIRED_MESSAGE, code="expired")
    except signing.BadSignature:
        raise ActivationError(
            INVALID_KEY_MESSAGE,
            code="invalid_key",
            params={"activation_key": activation_key},
        )


def get_user(self, username):
    User = get_user_model()
    try:
        user = User.objects.get(**{User.USERNAME_FIELD: username})
        if user.is_active:
            raise ActivationError(
                self.ALREADY_ACTIVATED_MESSAGE, code="already_activated"
            )
        return user
    except User.DoesNotExist:
        raise ActivationError(self.BAD_USERNAME_MESSAGE, code="bad_username")


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
