from django.contrib import admin
from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views. manager_landing, name='dashboard'),
    path('admin/', admin.site.urls),
    path('list/', views.product_list, name='product_list'),
    path('new/', views.product_form, name='product_form'),
    path('<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('entries/', views.inventory_entry, name='inventory_entry'),
    path('entries/manage/', views.inventory_entries, name='inventory_entries'),  # New path for managing entries
    path('entries/edit/<int:entry_id>/', views.edit_inventory_entry, name='edit_inventory_entry'),  # Edit entry
    path('entries/delete/<int:entry_id>/', views.delete_inventory_entry, name='delete_inventory_entry'),  # Delete entry
    path('sales/', views.sales_entry, name='sales_entry'),
    path('sales/manage/', views.sales_entries, name='sales_entries'),  # New path for managing sales
    path('sales/edit/<int:sale_id>/', views.edit_sales_entry, name='edit_sales_entry'),  # Edit sale
    path('sales/delete/<int:sale_id>/', views.delete_sales_entry, name='delete_sales_entry'),  # Delete sale
    path('status/', views.inventory_status, name='inventory_status'),
    path('bulk-operations/', views.bulk_operations, name='bulk_operations'),
    path('reorder/', views.reorder_page, name='reorder_page'),
    path('commandes/', views.order_list, name='commandes_list'),
    path('commandes/<int:order_id>/', views.order_details, name='commandes_details'),
    path('commandes/<int:order_id>/edit/', views.order_edit, name='commandes_edit'),
    path('commandes/<int:order_id>/delete/', views.order_delete, name='commandes_delete'),
    path('import/', views.import_products_from_csv, name='import_products'),
    path('inventory/export-pdf/', views.export_inventory_to_pdf, name='export_inventory_to_pdf'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/new/', views.new_invoice, name='new_invoice'),
    path('invoices/<int:invoice_id>/', views.invoice_details, name='invoice_details'),
    path('invoices/<int:invoice_id>/edit/', views.edit_invoice, name='edit_invoice'),
    path('invoices/<int:invoice_id>/delete/', views.delete_invoice, name='delete_invoice'),
    path('load/', views.load_inventory, name='load_inventory'),
    path('unload/', views.unload_inventory, name='unload_inventory'),
    path('sales-report/', views.sales_report, name='sales_report'),
    path('sales_report/<int:sale_id>/', views.sale_details, name='sale_details'),
    path('manager-inventory/', views.manager_inventory, name='manager_inventory'),
    path('seller-stock/', views.daily_seller_stock, name='daily_seller_stock'),
    path('seller-stock/load/', views.load_new_inventory, name='load_new_inventory'),
    path('seller-stock/unload/', views.unload_new_inventory, name='unload_new_inventory'),
    path('seller-sales-summary/', views.daily_sales_summary, name='daily_sales_summary'),
    path('seller-sales-summary/<int:seller_id>/<date>/', views.daily_sales_detail, name='daily_sales_detail'),
    path('unload-report/<int:seller_id>/<str:date>/', views.export_unload_pdf, name='export_unload_pdf'),
    path('dashboard/metrics/', views.metrics_dashboard, name='metrics_dashboard'),
    path('payments/', views.seller_payment_entry, name='seller_payment_entry'),
    path('payments/unpaid-report/', views.unpaid_balances_report, name='unpaid_balances_report'),
    path('payments/history/', views.seller_payment_history, name='seller_payment_history'),
    # Customer management
    path('clients/', views.customer_list, name='customer_list'),
    path('clients/add/', views.customer_create, name='customer_create'),
    # Order management
    path('orders/', views.customer_order_list, name='order_list'),
    path('orders/create/<int:customer_id>/', views.order_create, name='order_create'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/pdf/', views.order_pdf, name='order_pdf'),
    # urls.py
    path('orders/<int:order_id>/receipt/', views.order_receipt, name='order_receipt'),
    path('load-report/<int:seller_id>/<str:date>/', views.export_load_pdf, name='export_loading_pdf'),
    # Mobile pages : 
    # urls.py
    path('mobile/', views.mobile_landing, name='mobile_landing'),
    path('mobile/inventory/load/', views.mobile_load_inventory, name='mobile_load_inventory'),
    path('mobile/inventory/unload/', views.mobile_unload_inventory, name='mobile_unload_inventory'),
    path('mobile/inventory/status/', views.mobile_inventory_status, name='mobile_inventory_status'),
    path('mobile/clients/', views.mobile_clients, name='mobile_clients'),
    path('mobile/clients/create/', views.mobile_create_customer, name='mobile_create_customer'),
    path('mobile/orders/', views.mobile_orders, name='mobile_orders'),
    path('mobile/cash/', views.mobile_cash, name='mobile_cash'),
    path('mobile/orders/create/', views.mobile_create_order, name='mobile_create_order'),
    path('mobile/orders/<int:order_id>/', views.mobile_order_detail, name='mobile_order_detail'),
    # urls.py
    path('accounts/profile/', views.post_login_redirect, name='post_login_redirect'),
    # urls.py
    path('manager/', views.manager_landing, name='manager_landing'),



]
