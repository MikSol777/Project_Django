from django.shortcuts import render

def home_page(request):
    return render(request, 'catalog/home.html')

def contacts_page(request):
    return render(request, 'catalog/contacts.html')
