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

# forms.py
from django import forms
from .models import Invoice, InvoiceItem


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'date', 'details', 'status']
        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['product', 'unit_price', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


# forms.py
from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'category', 'amount', 'description', 'receipt']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

# forms.py

from .models import Revenue
from django import forms

class RevenueForm(forms.ModelForm):
    class Meta:
        model = Revenue
        fields = ['date', 'amount', 'category', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

from .models import CashFlowEntry
from django import forms

class CashFlowEntryForm(forms.ModelForm):
    class Meta:
        model = CashFlowEntry
        fields = ['date', 'type', 'amount', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# forms.py
from django import forms
from .models import DuePayment

class DuePaymentForm(forms.ModelForm):
    class Meta:
        model = DuePayment
        fields = ['supplier', 'due_date', 'amount', 'method', 'status', 'description']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }
