# Create your views here.
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
# from . models import Newinvoice,InvoiceItem,Product,BundleItem
from sowaf.models import Newcustomer


# Expenses view
def expenses(request):
   
    return render(request, 'expenses.html', {})
def add_time_activity(request):
   
    return render(request, 'time_activity_form.html', {})
def add_bill(request):
   
    return render(request, 'bill_form.html', {})
def purchase_order(request):
   
    return render(request, 'purchase_order_form.html', {})
def supplier_credit(request):
   
    return render(request, 'supplier_credit_form.html', {})
def add_expenses(request):
   
    return render(request, 'expenses_form.html', {})
def pay_down_credit(request):
   
    return render(request, 'pay_down_credit_form.html', {})
def import_bills(request):
   
    return render(request, 'import_bills_form.html', {})
def credit_card(request):
   
    return render(request, 'credit_card_credit_form.html', {})
def add_cheque(request):
   
    return render(request, 'cheque_form.html', {})


