from django import forms

from cafe.models import Product, Basket


class BasketEditForm(forms.Form):
    product_id = forms.IntegerField(required=True)
    product_count = forms.IntegerField(required=True)

    def clean_product_id(self):
        product_id = self.cleaned_data['product_id']
        if not Product.objects.filter(id=product_id).exists():
            raise forms.ValidationError('Invalid product ID')
        return product_id

    def clean_product_count(self):
        product_count = self.cleaned_data['product_count']
        if product_count == 0:
            raise forms.ValidationError('Invalid product count')
        return product_count


class OrderForm(forms.Form):
    basket_id = forms.IntegerField(required=True)

    def clean_basket_id(self):
        basket_id = self.cleaned_data['basket_id']
        if not Basket.objects.filter(id=basket_id).exists():
            raise forms.ValidationError('Invalid basket ID')
        return basket_id
