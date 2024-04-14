from django.conf import settings
from django.core.cache import cache

from catalog.models import Category, Product


def get_cached_categories():
    """
    Получает категории из кэша, если кэширование включено, иначе получает категории из базы данных.

    Returns:
        QuerySet: QuerySet объект, содержащий категории.
    """
    if settings.CACHE_ENABLED:
        key = "categories_list"
        categories_list = cache.get(key)
        if categories_list is None:
            categories_list = Category.objects.all()
            cache.set(key, categories_list, 60)
        return categories_list
    else:
        return Category.objects.all()


def get_cached_products():
    """
    Получает список продуктов из кэша, если кэширование включено, иначе получает продукты из базы данных.

    Returns:
        QuerySet: QuerySet объект, содержащий продукты.
    """
    if settings.CACHE_ENABLED:
        key = "products_list"
        products_list = cache.get(key)
        if products_list is None:
            products_list = Product.objects.all()
            cache.set(key, products_list, 60)
        return products_list
    else:
        return Product.objects.all()
