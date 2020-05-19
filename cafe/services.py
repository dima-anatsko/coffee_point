from cafe.models import Basket, Category, Product


def get_categories_pr_images():
    return Category.objects.prefetch_related('images_category')


def get_products_pr_images():
    return Product.objects.filter(published=True).prefetch_related(
        'images_product')


def get_basket_items_latest(user):
    return Basket.objects.filter(
        user=user
    ).prefetch_related('items').latest()


def get_category_request(request):
    return request.GET.get('category', Category.objects.first().slug)


def products_in_category(request):
    products = get_products_pr_images()
    if category := get_category_request(request):
        products = products.filter(category__slug=category)
    return products


def isbasket_or_create(user):
    if not Basket.objects.filter(user=user).exists():
        Basket.objects.create(user=user)


def get_total_cost_basket(basket):
    return round(
        sum(item.product.price * item.count for item in basket.items.all()), 2)
