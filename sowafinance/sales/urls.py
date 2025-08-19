from django.urls import path
from . import views


app_name='sales'
# my urls
urlpatterns = [  
# sales urls
    path('sales/', views.sales, name='sales'),
    path('sales/add/invoice', views.add_invoice, name='add-invoice'),
    path('sales/add/receipts', views.add_receipt, name='add-receipt'),
    path('sales/add/payments', views.add_payment, name='add-payments'),
    path('sales/add/products', views.add_products, name='add-products'),
    path('sales/add/invoice', views.add_invoice, name='add-invoice'),
    path('sales/invoices/', views.invoice_list, name='invoices'),
    path('sales/full-invoice-details/', views.full_invoice_details, name='full-invoice-details'),
    path('sales/individual-invoice/', views.individual_invoice, name='individual-invoice'),
    # path('receipts/', views.receipt, name='receipts'),
    path('receipts/add/receipt', views.add_receipt, name='add-receipt'),
    # path('payments/', views.payment, name='payments'),
    path('payments/add/payment', views.add_payment, name='add-payment'),
]
