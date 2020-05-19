from contextlib import suppress

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from cafe.forms import BasketEditForm, OrderForm
from cafe.models import Product, Basket, BasketItem, Shipment, Order
from cafe.services import get_basket_items_latest, isbasket_or_create, \
    get_total_cost_basket, get_categories_pr_images, get_category_request, \
    products_in_category


class HomePageView(LoginRequiredMixin, ListView):
    template_name = 'barista.html'

    def get_queryset(self):
        return products_in_category(self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['selected_category'] = get_category_request(self.request)
        context['categories'] = get_categories_pr_images()
        isbasket_or_create(self.request.user)
        with suppress(Basket.DoesNotExist):
            context['basket'] = get_basket_items_latest(self.request.user)
            context['total_cost'] = get_total_cost_basket(context['basket'])
        return context


class BasketEditView(LoginRequiredMixin, FormView):
    http_method_names = ['post']
    form_class = BasketEditForm

    def form_valid(self, form):
        try:
            basket = get_basket_items_latest(self.request.user)
        except Basket.DoesNotExist:
            basket = Basket.objects.create(user=self.request.user)

        product_id = form.cleaned_data['product_id']
        product_count = form.cleaned_data['product_count']
        basket_item = basket.items.filter(product_id=product_id).first()
        if basket_item:
            basket_item.count += product_count
            if basket_item.count <= 0:
                basket_item.delete()
            else:
                basket_item.save()
        else:
            BasketItem.objects.create(
                basket=basket,
                product_id=product_id
            )
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER') or reverse_lazy('home')


class OrderView(LoginRequiredMixin, FormView):
    http_method_names = ['post']
    form_class = OrderForm

    def form_valid(self, form):
        with suppress(Basket.DoesNotExist):
            basket = Basket.objects.filter(
                id=form.cleaned_data['basket_id']
            ).prefetch_related('items').first()
            basket_items = basket.items.all()
            if basket_items:
                Basket.objects.create(user=self.request.user)
            order_sum = 0
            order_cost = 0
            for item in basket_items:
                order_sum += round(item.count * item.product.price, 2)
                flow_charts = Product.objects.filter(
                    id=item.product.id
                ).prefetch_related('flow_chart').first()
                print(f'{item.product=}')
                for flow_chart in flow_charts.flow_chart.all():
                    shipment_of_cost = Shipment.objects.filter(
                        ingredient=flow_chart.ingredient,
                        warehouses__isnull=False).first()
                    if shipment_of_cost:
                        value_ingredient = flow_chart.value * item.count
                        warehouse = shipment_of_cost.warehouses.first()
                        if warehouse.value > value_ingredient:
                            warehouse.value -= value_ingredient
                            warehouse.save()
                        else:
                            warehouse.delete()
                    else:
                        # if the ingredient is not in stock we take its cost
                        # from the last purchase
                        shipment_of_cost = Shipment.objects.filter(
                            ingredient=flow_chart.ingredient).latest()
                    if shipment_of_cost:
                        cost_ingredient = shipment_of_cost.price
                    else:
                        cost_ingredient = 0
                    order_cost += round(
                        cost_ingredient * item.count * flow_chart.value, 2)
            Order.objects.create(
                basket=basket,
                price=order_sum,
                cost=order_cost
            )
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER') or reverse_lazy('home')
