from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, InventoryEntry, SalesEntry, Order
from .forms import ProductForm, InventoryEntryForm, SalesEntryForm
from django.db.models import Sum, Max, Q
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.utils.timezone import now
import uuid
from io import BytesIO
import csv
from django.db import IntegrityError
from products.models import Product

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import csv
from .models import Product
from django.db.models import Q


def product_form(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

def product_list(request):
    # Get query parameters for filtering
    category = request.GET.get('category')
    supplier = request.GET.get('supplier')

    # Filter products based on selected category and supplier
    products = Product.objects.all()
    if category:
        products = products.filter(category=category)
    if supplier:
        products = products.filter(supplier=supplier)

    # Get distinct categories and suppliers for the filter dropdowns
    categories = Product.objects.values_list('category', flat=True).distinct()
    suppliers = Product.objects.values_list('supplier', flat=True).distinct()

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'suppliers': suppliers,
        'selected_category': category,
        'selected_supplier': supplier,
    })

def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_edit.html', {'form': form, 'product': product})

def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('products:product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

def inventory_entry(request):
    if request.method == 'POST':
        form = InventoryEntryForm(request.POST)
        if form.is_valid():
            entry = form.save()
            if entry.entry_type == 'restock':
                entry.product.quantity += entry.quantity
            elif entry.entry_type == 'return':
                entry.product.quantity += entry.quantity
            entry.product.save()
            return redirect('products:inventory_entry')
    else:
        form = InventoryEntryForm()
    entries = InventoryEntry.objects.all().order_by('-date')
    return render(request, 'inventory/inventory_entry.html', {'form': form, 'entries': entries})

def sales_entry(request):
    if request.method == 'POST':
        form = SalesEntryForm(request.POST)
        if form.is_valid():
            sale = form.save()
            sale.product.quantity -= sale.quantity
            sale.product.save()
            return redirect('products:sales_entry')
    else:
        form = SalesEntryForm()
    sales = SalesEntry.objects.all().order_by('-date')
    return render(request, 'inventory/inventory_sales.html', {'form': form, 'sales': sales})

# Inventory Entries Management
def inventory_entries(request):
    entries = InventoryEntry.objects.all().order_by('-date')
    return render(request, 'inventory/inventory_entries.html', {'entries': entries})


def edit_inventory_entry(request, entry_id):
    entry = get_object_or_404(InventoryEntry, id=entry_id)
    if request.method == 'POST':
        form = InventoryEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory entry updated successfully!")
            return redirect('inventory:inventory_entries')
    else:
        form = InventoryEntryForm(instance=entry)
    return render(request, 'inventory/edit_inventory_entry.html', {'form': form, 'entry': entry})


def delete_inventory_entry(request, entry_id):
    entry = get_object_or_404(InventoryEntry, id=entry_id)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, "Inventory entry deleted successfully!")
        return redirect('products:inventory_entries')
    return render(request, 'inventory/delete_inventory_entry.html', {'entry': entry})


# Sales Entries Management
def sales_entries(request):
    sales = SalesEntry.objects.all().order_by('-date')
    return render(request, 'inventory/sales_entries.html', {'sales': sales})


def edit_sales_entry(request, sale_id):
    sale = get_object_or_404(SalesEntry, id=sale_id)
    if request.method == 'POST':
        form = SalesEntryForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            messages.success(request, "Sales entry updated successfully!")
            return redirect('products:sales_entries')
    else:
        form = SalesEntryForm(instance=sale)
    return render(request, 'inventory/edit_sales_entry.html', {'form': form, 'sale': sale})


def delete_sales_entry(request, sale_id):
    sale = get_object_or_404(SalesEntry, id=sale_id)
    if request.method == 'POST':
        sale.delete()
        messages.success(request, "Sales entry deleted successfully!")
        return redirect('inventory:sales_entries')
    return render(request, 'inventory/delete_sales_entry.html', {'sale': sale})


def inventory_status(request):
    # Get filter parameters
    category_filter = request.GET.get('category')
    supplier_filter = request.GET.get('supplier')

    # Filter products
    products = Product.objects.all()
    if category_filter:
        products = products.filter(category=category_filter)
    if supplier_filter:
        products = products.filter(supplier=supplier_filter)

    # Group products by category
    categories = Product.CATEGORY_CHOICES
    products_by_category = {
        category[0]: products.filter(category=category[0]) for category in categories
    }

    # Get distinct categories and suppliers for filters
    distinct_categories = Product.objects.values_list('category', flat=True).distinct()
    distinct_suppliers = Product.objects.values_list('supplier', flat=True).distinct()

    return render(request, 'inventory/inventory_status.html', {
        'products_by_category': products_by_category,
        'distinct_categories': distinct_categories,
        'distinct_suppliers': distinct_suppliers,
        'selected_category': category_filter,
        'selected_supplier': supplier_filter,
    })

def dashboard(request):
    total_products = Product.objects.count()
    total_stock_value = Product.objects.aggregate(
        total_value=Sum('quantity', field="quantity * purchase_price")
    )['total_value'] or 0
    total_sales_value = SalesEntry.objects.aggregate(
        total_sales=Sum('quantity', field="quantity * product__selling_price")
    )['total_sales'] or 0
    low_stock_products = Product.objects.filter(quantity__lt=5).count()

    recent_entries = InventoryEntry.objects.order_by('-date')[:5]
    recent_sales = SalesEntry.objects.order_by('-date')[:5]

    context = {
        'total_products': total_products,
        'total_stock_value': total_stock_value,
        'total_sales_value': total_sales_value,
        'low_stock_products': low_stock_products,
        'recent_entries': recent_entries,
        'recent_sales': recent_sales,
    }
    return render(request, 'inventory/dashboard.html', context)

def bulk_operations(request):
    if request.method == 'POST':
        operation = request.POST.get('operation')  # Get selected operation (sales or entry)
        quantities = {int(k.split('_')[1]): int(v) for k, v in request.POST.items() if k.startswith('quantity_') and v}

        with transaction.atomic():  # Ensure atomicity of bulk operation
            for product_id, quantity in quantities.items():
                product = Product.objects.get(id=product_id)
                if operation == 'entry':
                    product.quantity += quantity
                    InventoryEntry.objects.create(product=product, entry_type='restock', quantity=quantity)
                elif operation == 'sales':
                    product.quantity -= quantity
                    SalesEntry.objects.create(product=product, quantity=quantity)
                product.save()
        # Add success message
        messages.success(request, f"Bulk {operation.capitalize()} operation completed successfully!")

        return redirect('products:bulk_operations')  # Redirect to the same page after processing

    # Fetch products grouped by category
    categories = Product.objects.values_list('category', flat=True).distinct()
    products_by_category = {category: Product.objects.filter(category=category) for category in categories}

    return render(request, 'inventory/bulk_operations.html', {
        'products_by_category': products_by_category
    })

def generate_order_number():
    current_year = now().year % 100  # Get the last two digits of the current year, e.g., 2025 -> 25

    # Get the last order number for the current year
    last_order = Order.objects.filter(order_number__endswith=f"/{current_year}").aggregate(
        max_number=Max("order_number")
    )
    last_number = last_order["max_number"]

    if last_number:
        # Extract the XXXX part and increment it
        last_number_int = int(last_number.split("/")[0][2:])  # Extract XXXX from BCXXXX/YY
        next_number = last_number_int + 1
    else:
        # No orders for the current year, start from 0001
        next_number = 1

    # Format the order number as BCXXXX/YY
    return f"BC{next_number:04d}/{current_year}"

def reorder_page(request):
    if request.method == 'POST':
        # Get supplier and order data from the request
        supplier = request.POST.get('supplier', 'Unknown Supplier')
        products = Product.objects.all()  # Retrieve all products

        # Generate a unique order number
        order_number = generate_order_number()  # Reuse the generate_order_number function

        # Prepare products with non-zero quantities
        selected_products = [
            {
                'name': product.name,
                'purchase_price': product.purchase_price,
                'quantity': int(request.POST.get(f'quantity_{product.id}', '0') or '0'),
                'total': float(product.purchase_price) * int(request.POST.get(f'quantity_{product.id}', '0') or '0'),
            }
            for product in products
            if int(request.POST.get(f'quantity_{product.id}', '0') or '0') > 0
        ]

        # Calculate total amount
        total_amount = sum(product['total'] for product in selected_products)

        # Save the order to the database
        order = Order.objects.create(
            order_number=order_number,
            supplier=supplier,
            total_amount=total_amount,
        )

        # Generate PDF for the order
        context = {
            'order': order,
            'products': selected_products,
            'total_amount': total_amount,
        }

        response = generate_pdf('products/reorder_pdf.html', context)

        return response

    return render(request, 'products/reorder_page.html', {'products': Product.objects.all()})

def generate_pdf(template_path, context):
    template = render_to_string(template_path, context)
    pdf_file = BytesIO()
    pisa.CreatePDF(BytesIO(template.encode('UTF-8')), pdf_file)
    pdf_file.seek(0)
    return HttpResponse(pdf_file, content_type='application/pdf')

def order_list(request):
    query = request.GET.get('search', '')  # Get the search query from the request
    if query:
        orders = Order.objects.filter(Q(order_number__icontains=query))
    else:
        orders = Order.objects.all().order_by('-created_at')

    return render(request, 'products/order_list.html', {'orders': orders, 'search_query': query})

def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'products/order_details.html', {'order': order})

def order_edit(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        order.supplier = request.POST.get('supplier', order.supplier)
        order.status = request.POST.get('status', order.status)
        order.save()
        return redirect('products:order_list')

    return render(request, 'products/order_edit.html', {'order': order})

def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        order.delete()
        return redirect('products:order_list')

    return render(request, 'products/order_confirm_delete.html', {'order': order})

def import_products_from_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "The file uploaded is not a CSV file.")
            return render(request, 'products/import_products.html')

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            # import pdb; pdb.set_trace()
            for row in reader:
                try:
                    Product.objects.create(
                        code=row['\ufeffcode'],
                        name=row['name'],
                        name_ar=row.get('name_ar', None),
                        purchase_price=float(row['purchase_price']),
                        selling_price=float(row['selling_price']),
                        quantity=int(row['quantity']),
                        category=row['category'],
                        supplier=row['supplier']
                    )
                except Exception as e:
                    messages.error(request, f"Error importing product {row.get('name', 'Unknown')}: {str(e)}")
            messages.success(request, "Products imported successfully!")
        except Exception as e:
            messages.error(request, f"Error processing the file: {str(e)}")
        
        return render(request, 'products/import_products.html')
    
    # Render the upload page for GET requests
    return render(request, 'products/import_products.html')

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

def export_inventory_to_pdf(request):
    category = request.GET.get('category')
    supplier = request.GET.get('supplier')

    # Filter products based on selected category and supplier
    products = Product.objects.all()
    if category:
        products = products.filter(category=category)
    if supplier:
        products = products.filter(supplier=supplier)

    # Group products by category
    categories = Product.objects.values_list('category', flat=True).distinct()
    products_by_category = {cat: products.filter(category=cat) for cat in categories}

    context = {
        'products_by_category': products_by_category,
    }

    # Render PDF
    template_path = 'inventory/inventory_pdf.html'
    html = render_to_string(template_path, context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="inventory.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', content_type='text/plain')
    return response
