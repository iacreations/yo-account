from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from openpyxl import Workbook
from tempfile import NamedTemporaryFile
from datetime import datetime, timedelta
from django.utils import timezone
import openpyxl
import csv
import io
import os
from django.core.files import File
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Newinvoice,InvoiceItem,Product,BundleItem
from sowaf.models import Newcustomer


# sales view
def sales(request):
    products = Product.objects.all()
    invoices = Newinvoice.objects.all().prefetch_related('invoiceitem_set')  # Optimized for related items
    invoice_count = Newinvoice.objects.count()
    return render(request, 'Sales.html', {'invoices': invoices,'invoice_count': invoice_count,'products': products})

# invoice form view

def add_invoice(request):
    if request.method == 'POST':
        # Parse date strings to datetime.date format
        raw_invoice_date = request.POST.get('invoice_date')
        raw_invoice_due = request.POST.get('invoice_due')

        try:
            invoice_date = datetime.strptime(raw_invoice_date, "%B %d, %Y").date()
        except ValueError:
            invoice_date = timezone.now().date()

        try:
            invoice_due = datetime.strptime(raw_invoice_due, "%B %d, %Y").date()
        except ValueError:
            invoice_due = timezone.now().date()

        invoice = Newinvoice.objects.create(
            invoice_id=request.POST.get('invoice_id'),
            invoice_date=invoice_date,
            invoice_due=invoice_due,
            customer_id=request.POST.get('customer'),
            email=request.POST.get('email'),
            billing_address=request.POST.get('billing_address'),
            shipping_address=request.POST.get('shipping_address'),
            terms=request.POST.get('terms'),
            sales_rep=request.POST.get('sales_rep'),
            location=request.POST.get('location'),
            tags=request.POST.get('tags'),
            po_number=request.POST.get('po_number'),
            memo=request.POST.get('memo'),
            customs_notes=request.POST.get('customs_notes'),
            attachments=request.FILES.get('attachments'),
            subtotal=request.POST.get('subtotal') or 0,
            discount=request.POST.get('discount') or 0,
            tax=request.POST.get('tax') or 0,
            shipping=request.POST.get('shipping') or 0,
            total_due=request.POST.get('total_due') or 0,
        )

        products = request.POST.getlist('product[]')
        descriptions = request.POST.getlist('description[]')
        qtys = request.POST.getlist('qty[]')
        rates = request.POST.getlist('rate[]')
        amounts = request.POST.getlist('amount[]')
        tax_checkboxes = request.POST.getlist('tax[]')

        for i in range(len(products)):
            InvoiceItem.objects.create(
                invoice=invoice,
                product=products[i],
                description=descriptions[i],
                qty=qtys[i] or 0,
                rate=rates[i] or 0,
                amount=amounts[i] or 0,
                tax='true' in tax_checkboxes[i] if i < len(tax_checkboxes) else False
            )

        save_action = request.POST.get("save_action")
        if save_action == "save&new":
            return redirect("sowaf:add-invoice")
        elif save_action == "save&close":
            return redirect("sales:sales")

        return redirect("sales:add-invoice")

    # GET: render form with pre-filled dates (in YYYY-MM-DD format)
    customers = Newcustomer.objects.all()
    today = timezone.now().date().strftime('%B-%d-%Y')       # <-- format to string
    due_date = (timezone.now().date() + timezone.timedelta(days=30)).strftime('%B-%d-%Y')  # <-- format

    last_invoice = Newinvoice.objects.order_by('-id').first()
    next_invoice_id = 1000 if not last_invoice else int(last_invoice.invoice_id) + 1

    return render(request, 'invoice_form.html', {
        'customers': customers,
        'today': today,
        'due_date': due_date,
        'next_invoice_id': next_invoice_id,
    })
#  invoice list
def invoice_list(request):
    invoices=Newinvoice.objects.all()
    customers=Newcustomer.objects.all()
    return render(request, 'invoice_lists.html',{
        'invoices':invoices,
        'customers':customers
    })
def full_invoice_details(request):
    invoices=Newinvoice.objects.all()
    customers=Newcustomer.objects.all()
    return render(request, 'full_invoice_details.html',{
        'invoices':invoices,
        'customers':customers
    })
def individual_invoice(request):
    return render(request, 'individual_invoice.html',{})
# receipt form view

def add_receipt(request):
    
    return render(request, 'receipt_form.html', {})
# receive payment form view

def add_payment(request):
    
    return render(request, 'receive_payment_form.html', {})
#add new product form view

def add_products(request):
    if request.method == "POST":
        type = request.POST.get("type")
        name = request.POST.get("name")
        sku = request.POST.get("sku")
        category = request.POST.get("category")
        class_field = request.POST.get("class_field")
        description = request.POST.get("description")
        sell_checkbox = request.POST.get("sellCheckbox") == 'on'
        sales_price = request.POST.get("sales_price")
        income_account = request.POST.get("income_account")
        purchase_checkbox = request.POST.get("purchaseCheckbox") == 'on'
        display_bundle_contents = request.POST.get("displayBundleContents") == 'on'

        products = Product.objects.create(
            type=type,
            name=name,
            sku=sku,
            category=category,
            class_field=class_field,
            description=description,
            sell_checkbox=sell_checkbox,
            sales_price=sales_price or None,
            income_account=income_account,
            purchase_checkbox=purchase_checkbox,
            is_bundle=(type == "Bundle"),
            display_bundle_contents=display_bundle_contents,
        )

        # Handle bundle items
        if type == "Bundle":
            names = request.POST.getlist("bundle_product_name[]")
            quantities = request.POST.getlist("bundle_product_qty[]")
            for name, qty in zip(names, quantities):
                BundleItem.objects.create(
                    bundle=products,
                    product_name=name,
                    quantity=qty
                )

        # Handle Save action
        action = request.POST.get("save_action")
        if action == "save&new":
            return redirect('sales:add-product')
        elif action == "save&close":
            return redirect()  # You should have this view
        return redirect('sales:sales')
    
    return render(request, 'Products_and_services_form.html', {})

