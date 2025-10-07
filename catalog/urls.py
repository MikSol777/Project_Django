from django.urls import path
from .views import home_page, contacts_page

urlpatterns = [
    path('', home_page, name='home_page'),
    path('contacts/', contacts_page, name='contacts_page')
]