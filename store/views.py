from .models import Product
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm
from .forms import OrderCreateForm
from .models import OrderItem
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order


def catalog(request):
    products = Product.objects.all()

    # filter
    if "type" in request.GET:
        products = products.filter(type__in=request.GET.getlist("type"))
    if "manufacturer" in request.GET:
        products = products.filter(manufacturer__title__in=request.GET.getlist("manufacturer"))

    # Paginate

    paginator = Paginator(products, 3)
    # if "type" in response:
    #     page_number = request.GET.get('page', 'type')
    # if "manufacturer" in response:
    #     page_number = request.GET.get('page', 'manufacturer')
    # else:
    page_number = request.GET.get('page',)
    page_obj = paginator.get_page(page_number)
    type = Product.type
    manufacturer = Product.manufacturer
    return render(request, 'store/catalog.html', {'page_obj': page_obj, 'type': type, 'manufacturer': manufacturer})


def services(request):
    return render(request, 'store/services.html')


def search(request):
    search_params = request.GET['search']
    query = Product.objects.filter(title__icontains=search_params)
    return render(request, 'store/catalog.html', {'query': query})


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


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
             OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'store/order_created.html', {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'store/order_create.html', {'cart': cart, 'form': form})
