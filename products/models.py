from django.db import models
# models.py
from django.db import models
from django.utils.timezone import now


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Fromages', 'Fromages'),
        ('Sauces', 'Sauces'),
        ('Poisson', 'Poisson'),
        ('Poulet', 'Poulet'),
        ('Divers', 'Divers'),
    ]

    SUPPLIER_CHOICES = [
        ('Top Chef', 'Top Chef'),
        ('Ali', 'Ali'),
        ('Adnane', 'Adnane'),
        ('Yozi Food', 'Yozi Food'),
        ('Divers', 'Divers'),
    ]

    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Divers')
    supplier = models.CharField(max_length=20, choices=SUPPLIER_CHOICES, default='Divers')
    critical_threshold = models.IntegerField(default=10)


    def __str__(self):
        return self.name

        return self.name

class InventoryEntry(models.Model):
    ENTRY_TYPES = [
        ('restock', 'Entree'),
        ('return', 'Retour'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPES)
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.entry_type.capitalize()} - {self.product.name}"

class SalesEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Sold - {self.product.name}"

class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    supplier = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Pending")  # e.g., Pending, Completed

    def __str__(self):
        return f"Order #{self.order_number} - {self.supplier}"

class Invoice(models.Model):
    client = models.CharField(max_length=255)
    date = models.DateField(default=now)
    details = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')

    def __str__(self):
        return f"Invoice {self.id} - {self.client}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

from django.contrib.auth.models import User

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class SellerInventory(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('seller', 'product')

    def __str__(self):
        return f"{self.seller.name} - {self.product.name}: {self.quantity}"

class LoadingRecord(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.seller.name} loaded {self.quantity} {self.product.name} on {self.date}"

class UnloadingRecord(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.seller.name} returned {self.quantity} {self.product.name} on {self.date}"


class SalesRecord(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.seller.name} sold {self.quantity_sold} {self.product.name} on {self.date}"


from django.db import models
from django.utils.timezone import now

class SellerProductDayEntry(models.Model):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    date = models.DateField(default=now)
    
    voiture = models.IntegerField(default=0)  # Remaining from yesterday
    sortie = models.IntegerField(default=0)   # Taken from warehouse
    retour = models.IntegerField(default=0)   # Returned to warehouse

    vendu = models.IntegerField(default=0)    # Computed field: voiture + sortie - retour
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # vendu * selling_price

    class Meta:
        unique_together = ('seller', 'product', 'date')

    def save(self, *args, **kwargs):
        self.vendu = self.voiture + self.sortie - self.retour
        self.amount = self.vendu * self.product.selling_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.seller.name} - {self.product.name}"


# products/models.py

from django.db import models
from django.utils.timezone import now

class DailySellerStockRecord(models.Model):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    date = models.DateField(default=now)

    voiture = models.IntegerField(default=0)  # Quantité restante de la veille
    sortie = models.IntegerField(default=0)   # Quantité chargée
    retour = models.IntegerField(default=0)   # Quantité non vendue (retour)
    vendu = models.IntegerField(default=0)    # vendu = voiture + sortie - retour

    class Meta:
        unique_together = ('seller', 'product', 'date')

    def save(self, *args, **kwargs):
        self.vendu = self.voiture + self.sortie - self.retour
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} | {self.seller.name} | {self.product.name} : vendu {self.vendu}"

# products/forms.py
from django import forms
from .models import DailySellerStockRecord

class DailySellerStockForm(forms.ModelForm):
    class Meta:
        model = DailySellerStockRecord
        fields = ['seller', 'product', 'date', 'voiture', 'sortie', 'retour']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

# products/models.py
from django.db import models
from django.utils.timezone import now
from .models import Seller

class SellerPayment(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    expected_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('seller', 'date')

    @property
    def balance(self):
        return self.expected_amount - self.paid_amount

    def __str__(self):
        return f"{self.seller.name} - {self.date}"

from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='customers')

    def __str__(self):
        return f"{self.name} ({self.seller.name})"

class CustomerOrder(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name} - {self.date.strftime('%Y-%m-%d')}"

class CustomerOrderItem(models.Model):
    order = models.ForeignKey(CustomerOrder, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.unit_price = self.product.selling_price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x{self.quantity} = {self.total_price} DH"
