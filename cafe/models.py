import base64

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
        ordering = ('title',)

    def __str__(self):
        return self.title


class Base64ImageMixin:
    def save(self, *args, **kwargs):
        if self.image:
            self.image_base64 = 'data:{content_type};base64,{data}'.format(
                content_type='jpeg',
                data=base64.b64encode(
                    self.image.file.read()
                ).decode()
            )
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        return self.image_base64 or self.image.url


class CategoryImage(Base64ImageMixin, models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to='categories/%Y/%m/%d/')
    image_base64 = models.TextField(default=None, null=True, blank=True)
    category = models.ForeignKey(
        'cafe.Category',
        related_name='images_category',
        on_delete=models.CASCADE
    )


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
    date = models.DateTimeField(verbose_name='Дата поставки', auto_now_add=True)
    ingredient = models.ForeignKey(
        'cafe.Ingredient',
        on_delete=models.CASCADE,
        related_name='shipments',
        verbose_name='Ингридиент'
    )
    value = models.FloatField(verbose_name='Количество')
    price = models.FloatField(verbose_name='Цена')
    shelf_life = models.DateTimeField(verbose_name='Срок годности')

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'
        get_latest_by = 'date'
        ordering = ('date',)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        shipment = Shipment.objects.latest('date')
        Warehouse.objects.create(shipment=shipment, value=shipment.value)

    def __str__(self):
        return self.ingredient.title


class Warehouse(models.Model):
    shipment = models.ForeignKey(
        'cafe.Shipment',
        on_delete=models.CASCADE,
        related_name='warehouses',
        verbose_name='Ингридиент'
    )
    value = models.FloatField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.shipment.ingredient.title


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

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('title',)

    def __str__(self):
        return self.title


class ProductImage(Base64ImageMixin, models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    image_base64 = models.TextField(default=None, null=True, blank=True)
    product = models.ForeignKey(
        'cafe.Product',
        related_name='images_product',
        on_delete=models.CASCADE
    )


class ProductIngredient(models.Model):
    product = models.ForeignKey(
        'cafe.Product',
        related_name='flow_chart',
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    ingredient = models.ForeignKey(
        'cafe.Ingredient',
        related_name='flow_chart',
        on_delete=models.CASCADE,
        verbose_name='Ингридиент'
    )
    value = models.FloatField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.product} {self.ingredient}'

    class Meta:
        verbose_name = 'Технологическая карта'
        verbose_name_plural = 'Технологические карты'


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='baskets'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина {self.user}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        get_latest_by = 'created_at'


class BasketItem(models.Model):
    basket = models.ForeignKey(
        'cafe.Basket',
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'cafe.Product',
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    count = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине'
        ordering = ('id', )


class Order(models.Model):
    basket = models.ForeignKey(
        'cafe.Basket',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(verbose_name='Продажа', default=0)
    cost = models.FloatField(verbose_name='Закупка', default=0)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'заказы'


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

    class Meta:
        verbose_name = 'Списание продукта'
        verbose_name_plural = 'Списание продуктов'
