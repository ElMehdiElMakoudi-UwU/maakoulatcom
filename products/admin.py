from django.contrib import admin
from .models import Product, InventoryEntry, SalesEntry, Order, Seller, SellerInventory, UnloadingRecord

# Register all models in Django Admin
admin.site.register(Product)
admin.site.register(InventoryEntry)
admin.site.register(SalesEntry)
admin.site.register(Order)
admin.site.register(Seller)
admin.site.register(SellerInventory)
admin.site.register(UnloadingRecord)
