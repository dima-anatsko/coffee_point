from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Наименование'
    )
    slug = models.SlugField(verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Ingredient(models.Model):

    class MeasureUnit(models.TextChoices):
        THING = 'TH', 'Шт.'
        LITER = 'LI', 'Литр'
        KILOGRAM = 'KI', 'Кг.'

    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Наименование'
    )
    measure_unit = models.CharField(
        max_length=2,
        choices=MeasureUnit.choices,
        default=MeasureUnit.THING,
        verbose_name='Ед. измерения'
    )
    notify_min_balance = models.FloatField(
        verbose_name='Минимальный остаток для оповещения',
        default=0
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.title


class Shipment(models.Model):
    date = models.DateTimeField(verbose_name='Срок годности', auto_now_add=True)
    ingredient = models.ForeignKey(
        'cafe.Ingredient',
        on_delete=models.CASCADE,
        related_name='shipments'
    )
    value = models.FloatField(verbose_name='Количество')
    price = models.FloatField(verbose_name='Цена')
    shelf_life = models.DateTimeField(verbose_name='Срок годности')

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'


class Warehouse(models.Model):
    shipment = models.ForeignKey(
        'cafe.Shipment',
        on_delete=models.CASCADE,
        related_name='warehouses'
    )
    value = models.FloatField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class Product(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Наименование'
    )
    price = models.FloatField(verbose_name='Цена')
    published = models.BooleanField(default=False, verbose_name='Опубликовать')
    category = models.ForeignKey(
        'cafe.Category',
        on_delete=models.CASCADE,
        related_name='products'
    )
    cost = models.FloatField(verbose_name='Себестоимость', default=0)


class ProductIngredient(models.Model):
    product = models.ForeignKey(
        'cafe.Product',
        related_name='flow_chart',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        'cafe.Ingredient',
        related_name='flow_chart',
        on_delete=models.CASCADE)
    value = models.FloatField(default=1)


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='baskets'
    )
    created_at = models.DateTimeField(auto_now_add=True)


class BasketItem(models.Model):
    basket = models.ForeignKey(
        'cafe.Basket',
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'cafe.Product',
        related_name='items',
        on_delete=models.CASCADE
    )
    count = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество'
    )


class Order(models.Model):
    basket = models.ForeignKey(
        'cafe.Basket',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(verbose_name='Продажа', default=0)
    cost = models.FloatField(verbose_name='Закупка', default=0)


class DestructionIngredient(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users'
    )
    warehouse = models.ForeignKey(
        'cafe.Warehouse',
        on_delete=models.CASCADE,
        related_name='warehouses'
    )
