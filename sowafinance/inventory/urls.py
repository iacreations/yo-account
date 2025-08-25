from django.urls import path
from . import views


app_name='inventory'
# my urls
urlpatterns = [ 
path('inventory/products', views.add_products, name='add-products'),
]