from django import forms
from django.forms import formset_factory

from billing.models import Product


class BillingForm(forms.Form):
    customer_email = forms.EmailField()
    cash_received = forms.DecimalField(max_digits=12, decimal_places=2)


class ProductLineForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        empty_label="-- Select Product --",
        widget=forms.Select(attrs={"class": "product-select"})
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "qty-input"})
    )


ProductLineFormSet = formset_factory(ProductLineForm, extra=1, can_delete=True)


class DenominationForm(forms.Form):
    d500 = forms.IntegerField(required=False, initial=0, min_value=0)
    d50 = forms.IntegerField(required=False, initial=0, min_value=0)
    d20 = forms.IntegerField(required=False, initial=0, min_value=0)
    d10 = forms.IntegerField(required=False, initial=0, min_value=0)
    d5 = forms.IntegerField(required=False, initial=0, min_value=0)
    d2 = forms.IntegerField(required=False, initial=0, min_value=0)
    d1 = forms.IntegerField(required=False, initial=0, min_value=0)
