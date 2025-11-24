from __future__ import annotations

from typing import Iterable, List

from django.conf import settings
from django.core.cache import cache

from .models import Product

PRODUCT_LIST_CACHE_KEY = 'catalog:home_products'
PRODUCT_LIST_CACHE_TIMEOUT = 300  # 5 минут


def get_products_by_category(category_id: int) -> Iterable[Product]:
    """
    Возвращает список продуктов, относящихся к указанной категории.
    Отдельная сервисная функция упрощает переиспользование логики в представлениях.
    """
    return (
        Product.objects.select_related('category')
        .filter(category_id=category_id)
        .order_by('name')
    )


def get_cached_products_list() -> List[Product]:
    """
    Возвращает список продуктов для главной страницы, используя низкоуровневый кеш.
    """
    if not settings.CACHE_ENABLED:
        return list(Product.objects.select_related('category').all())

    products = cache.get(PRODUCT_LIST_CACHE_KEY)
    if products is None:
        products = list(Product.objects.select_related('category').all())
        cache.set(PRODUCT_LIST_CACHE_KEY, products, PRODUCT_LIST_CACHE_TIMEOUT)
    return products


def invalidate_products_cache() -> None:
    """
    Сбрасывает кеш главного списка продуктов при любых изменениях в товарах.
    """
    cache.delete(PRODUCT_LIST_CACHE_KEY)


