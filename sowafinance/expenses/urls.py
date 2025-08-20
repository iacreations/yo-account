from django.urls import path
from . import views
app_name='expenses'
# my urls
urlpatterns = [  
# expenses urls
    path('expenses/', views.expenses, name='expenses'),
    path('expenses/add/time-activity', views.add_time_activity, name='time-activity'),
    path('expenses/add/bill', views.add_bill, name='add-bill'),
    path('expenses/supplier-credit', views.supplier_credit, name='supplier-credit'),
    path('expenses/add/purchase_order', views.purchase_order, name='purchase_order'),
    path('expenses/pay_down_credit', views.pay_down_credit, name='pay-down-credit'),
    path('expenses/import_bills', views.import_bills, name='import-bills'),
    path('expenses/credit_card', views.credit_card, name='credit-card'),
    path('expenses/add/cheque', views.add_cheque, name='add-cheque'),
    path('expenses/add/expenses', views.add_expenses, name='add-expenses'),
]
