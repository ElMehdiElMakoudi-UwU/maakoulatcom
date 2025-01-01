from django.contrib import admin
from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('list/', views.product_list, name='product_list'),
    path('new/', views.product_form, name='product_form'),
    path('<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('entries/', views.inventory_entry, name='inventory_entry'),
    path('sales/', views.sales_entry, name='sales_entry'),
    path('status/', views.inventory_status, name='inventory_status'),
    path('bulk-operations/', views.bulk_operations, name='bulk_operations'),
    path('reorder/', views.reorder_page, name='reorder_page'),
]
