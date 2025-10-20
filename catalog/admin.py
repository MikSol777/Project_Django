from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')              # показываем id и name
    search_fields = ('name', 'description')    # поиск по name и description


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')  # показываем эти поля в списке
    list_filter = ('category',)                        # фильтр по категории
    search_fields = ('name', 'description')             # поиск по name и description
