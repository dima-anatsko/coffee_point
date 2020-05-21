from django import forms
from django.utils import timezone

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


class ReportEditForm(forms.Form):
    from_date = forms.DateField(required=True)
    to_date = forms.DateField(required=True)

    def clean_from_date(self):
        from_date = self.cleaned_data['from_date']
        if from_date > timezone.now().date():
            raise forms.ValidationError('Дата не должна быть больше текущей')
        return from_date

    def clean_to_date(self):
        to_date = self.cleaned_data['to_date']
        if to_date > timezone.now().date():
            raise forms.ValidationError('Дата не должна быть больше текущей')
        return to_date
