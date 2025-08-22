from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from openpyxl import Workbook
from tempfile import NamedTemporaryFile
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal
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
from accounts.utils import record_sale


# sales view
def sales(request):
    products = Product.objects.all()
    invoices = Newinvoice.objects.all().prefetch_related('invoiceitem_set')  # Optimized for related items
    invoice_count = Newinvoice.objects.count()
    return render(request, 'Sales.html', {'invoices': invoices,'invoice_count': invoice_count,'products': products})

# invoice form view

def add_invoice(request):
    if request.method == "POST":
        # Parse customer and invoice info
        customer_id = request.POST.get('customer')
        customer=None
        if customer_id:
            try:
                customer = Newcustomer.objects.get(pk=customer_id)
            except Newcustomer.DoesNotExist:
                customer=None
        memo = request.POST.get("memo")
        customs_notes = request.POST.get("customs_notes")
        product_id = request.POST.get('product')
        product=None
        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                product=None
        subtotal = Decimal(request.POST.get("subtotal") or 0)
        discount = Decimal(request.POST.get("discount") or 0)
        shipping = Decimal(request.POST.get("shipping") or 0)

        # Invoice totals
        total_tax = Decimal("0")
        total_due = Decimal("0")

        # Create invoice
        invoice = Newinvoice.objects.create(
            customer=customer,
            memo=memo,
            product=product,
            customs_notes=customs_notes,
            subtotal=subtotal,
            discount=discount,
            tax=0,  # will update after items
            shipping=shipping,
            total_due=0,  # will update later
        )

        # Process line items
        products = request.POST.getlist("product[]")
        descriptions = request.POST.getlist("description[]")
        qtys = request.POST.getlist("qty[]")
        rates = request.POST.getlist("rate[]")
        tax_checks = request.POST.getlist("tax-check") 
        # calling in the line items
        for i in range(len(products)):
            qty = Decimal(qtys[i] or 0)
            rate = Decimal(rates[i] or 0)
            amount = qty * rate
     # checking if the tax check box is checked
            is_taxable = str(i) in tax_checks or "on" in tax_checks  # adjust parsing
            tax_amount = amount * Decimal("0.18") if is_taxable else Decimal("0.00")
#  saving the invoice products
            InvoiceItem.objects.create(
                invoice=invoice,
                product=products[i],
                description=descriptions[i],
                qty=qty,
                rate=rate,
                amount=amount,
                tax=tax_amount
            )

            total_tax += tax_amount
            total_due += amount + tax_amount

        # Apply discount and shipping
        total_due = total_due * (1 - discount/100) + shipping

        # Update invoice totals
        invoice.tax = total_tax
        invoice.total_due = total_due
        invoice.save()

        # Post to CoA
        record_sale(invoice)

        # Decide redirect
        save_action = request.POST.get("save_action")
        if save_action == "save&new":
            return redirect("sales:add-invoice")
        elif save_action == "save&close":
            return redirect("sales:sales")

        return redirect("sales:add-invoice")

    # GET: show form
    today = timezone.now().date()
    due_date = today + timezone.timedelta(days=30)

    last_invoice = Newinvoice.objects.order_by("-id").first()
    next_invoice_id = 1000 if not last_invoice else int(last_invoice.invoice_id) + 1

    products = Product.objects.all()  # for dropdown
    customers = Newcustomer.objects.all()

    return render(request, "invoice_form.html", {
        "customers": customers,
        "today": today.strftime("%d-%m-%Y"),
        "due_date": due_date.strftime("%d-%m-%Y"),
        "next_invoice_id": next_invoice_id,
        "products": products,
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
            return redirect('sales:sales')  # You should have this view
        return redirect('sales:sales')
    
    return render(request, 'Products_and_services_form.html', {})

