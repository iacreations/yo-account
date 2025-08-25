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
from . models import Product,BundleItem
from accounts.utils import record_sale

# Create your views here.

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
            return redirect('inventory:add-products')
        elif action == "save&close":
            return redirect('sales:sales')  # You should have this view
        return redirect('sales:sales')
    
    return render(request, 'Products_and_services_form.html', {})

