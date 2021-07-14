from .models import Product
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404


def catalog(request):
    contact_list = Product.objects.all()

    # filter
    if "type" in request.GET:
        contact_list = contact_list.filter(type__in=request.GET.getlist("type"))
    if "manufacturer" in request.GET:
        contact_list = contact_list.filter(manufacturer__title__in=request.GET.getlist("manufacturer"))

    # Paginate

    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'store/catalog.html', {'page_obj': page_obj})


def services(request):
    return render(request, 'store/services.html')


def search(request):
    search_params = request.GET['search']
    query = Product.objects.filter(title__icontains=search_params)
    return render(request, 'store/catalog.html', {'query': query})


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product.html', {'product': product})
