from django import forms
from .models import Product

from django import forms
from .models import InventoryEntry, SalesEntry

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'purchase_price', 'selling_price', 'category', 'supplier']


class InventoryEntryForm(forms.ModelForm):
    class Meta:
        model = InventoryEntry
        fields = ['product', 'entry_type', 'quantity']


class SalesEntryForm(forms.ModelForm):
    class Meta:
        model = SalesEntry
        fields = ['product', 'quantity']
