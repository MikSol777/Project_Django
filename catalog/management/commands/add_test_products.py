from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Добавляет тестовые категории и продукты в базу'

    def handle(self, *args, **options):
        # Удаляем существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.WARNING('Все существующие данные удалены'))

        # Создаём категории
        cat1 = Category.objects.create(name='Электроника', description='Все электронные товары')
        cat2 = Category.objects.create(name='Одежда', description='Мужская и женская одежда')
        cat3 = Category.objects.create(name='Книги', description='Книги разных жанров')

        # Создаём продукты
        Product.objects.create(name='Ноутбук', description='Игровой ноутбук', price=110000, category=cat1)
        Product.objects.create(name='Смартфон', description='Флагманский смартфон', price=80000, category=cat1)
        Product.objects.create(name='Футболка', description='Хлопковая футболка', price=1200, category=cat2)
        Product.objects.create(name='Python книга', description='Учебник по Python', price=1500, category=cat3)

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно добавлены'))
