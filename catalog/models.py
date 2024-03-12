from django.db import models


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

    def __str__(self):
        return f'{self.product_name}'

    class Meta:
        verbose_name = ("Товар")
        verbose_name_plural = ("Товары")
