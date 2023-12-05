from django.shortcuts import render
from .models import Product, Category
from .forms import CartAddProductForm


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'Vers/Page.html', {
        'products': products,
        'categories': categories
    })


def category_index(request, category):
    category = Category.objects.get(slug=category)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'Vers/Page.html', {
        'products': products,
        'categories': categories
    })


def look_product(request, product):
    product = Product.objects.get(slug=product)
    categories = Category.objects.all()
    add_form = CartAddProductForm
    return render(request, 'Vers/Look.html', {
        "product": product,
        'categories': categories,
        'add_form': add_form

    })
