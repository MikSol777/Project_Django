from django.urls import path
from .views import home_page, contacts_page, product_detail

urlpatterns = [
    path('', home_page, name='home_page'),
    path('contacts/', contacts_page, name='contacts_page'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
]
