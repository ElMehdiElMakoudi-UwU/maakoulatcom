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
from .models import CashFlowEntry

@admin.register(CashFlowEntry)
class CashFlowEntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'amount', 'description')
    list_filter = ('type', 'date')
    search_fields = ('description',)
