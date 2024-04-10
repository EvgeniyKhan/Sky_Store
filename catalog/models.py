from django.db import models
from django.conf import settings

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='Наименование категории')
    category_description = models.TextField(max_length=300, verbose_name='Описание категории', **NULLABLE)

    def __str__(self):
        return f'{self.category_name} {self.category_description}'

    class Meta:
        verbose_name = ("Категория")
        verbose_name_plural = ("Категории")


class Product(models.Model):
    product_name = models.CharField(max_length=50, verbose_name='Наименование')
    description = models.TextField(max_length=300, verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='preview/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена за покупку')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания', **NULLABLE)
    updated_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения', **NULLABLE)
    publication = models.BooleanField(default=False, verbose_name='Опубликовано')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.product_name}'

    class Meta:
        verbose_name = ("Товар")
        verbose_name_plural = ("Товары")
        permissions = [
            ('change_description_product', 'Change description'),
            ('change_categories_product', 'Change category'),
            ('change_publication_product', 'Change publication')
        ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    numbers_version = models.IntegerField(verbose_name='Номер версии')
    name = models.CharField(verbose_name='Название версии')
    is_active = models.BooleanField(default=False, verbose_name='Активная версия')

    def __str__(self):
        return f'{self.numbers_version}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
