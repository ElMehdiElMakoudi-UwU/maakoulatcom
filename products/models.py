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

class Seller(models.Model):
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
