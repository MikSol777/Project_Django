from django.shortcuts import render, get_object_or_404
from .models import Product

def home_page(request):
    products = Product.objects.all()  # ← получаем все товары из базы
    return render(request, 'catalog/home.html', {'products': products})

def contacts_page(request):
    return render(request, 'catalog/contacts.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})
