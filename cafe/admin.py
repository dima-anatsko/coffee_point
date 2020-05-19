from django.contrib import admin

from cafe.models import ProductImage, Product, Category, CategoryImage, \
    Ingredient, Shipment, Warehouse, ProductIngredient, Basket, BasketItem, \
    Order, DestructionIngredient


class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    fields = ('description', 'image', 'image_base64')
    extra = 0
    min_num = 0
    max_num = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = (CategoryImageInline,)
    list_display = ('title', 'slug')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ('description', 'image', 'image_base64')
    extra = 0
    min_num = 0
    max_num = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImageInline, )
    list_display = ('title', 'category', 'price', 'published')
    ordering = ('title',)
    search_fields = ('title',)
    list_filter = ('title', 'category', 'published', )
    list_editable = ('price',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'measure_unit', 'notify_min_balance')
    ordering = ('title',)
    search_fields = ('title',)
    list_filter = ('title', 'measure_unit',)
    list_editable = ('notify_min_balance', )


class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'value', 'price', 'date', 'shelf_life')
    ordering = ('ingredient', )
    search_fields = ('ingredient', 'date', 'shelf_life', )
    list_filter = ('ingredient', 'date', 'shelf_life', )


class WarehouseAdmin(admin.ModelAdmin):
    list_display = (
        'shipment',
        'value',
        'shipment_price',
        'shipment_date',
        'shipment_shelf_life',
    )
    ordering = ('shipment', )
    search_fields = ('shipment', 'shipment_date', 'shipment_shelf_life', )
    list_filter = ('shipment', 'shipment__date', 'shipment__shelf_life', )

    def shipment_price(self, obj):
        return obj.shipment.price
    shipment_price.admin_order_field = 'shipment__price'
    shipment_price.short_description = 'Цена'

    def shipment_date(self, obj):
        return obj.shipment.date
    shipment_date.admin_order_field = 'shipment__date'
    shipment_date.short_description = 'Дата поставки'

    def shipment_shelf_life(self, obj):
        return obj.shipment.shelf_life
    shipment_shelf_life.admin_order_field = 'shipment__shelf_life'
    shipment_shelf_life.short_description = 'Срок годности'


class ProductIngredientAdmin(admin.ModelAdmin):
    list_display = ('product', 'ingredient', 'value', 'ingredient_measure_unit')
    ordering = ('product', )
    search_fields = ('ingredient', 'product', )
    list_filter = ('ingredient', 'product', )

    def ingredient_measure_unit(self, obj):
        return dict(Ingredient.MeasureUnit.choices)[obj.ingredient.measure_unit]
    ingredient_measure_unit.admin_order_field = 'ingredient__measure_unit'
    ingredient_measure_unit.short_description = 'Ед. измерения'


class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'basket', 'created_at', 'price', 'cost')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(ProductIngredient, ProductIngredientAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(BasketItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(DestructionIngredient)
