from django.contrib import admin
from . models import Newinvoice,InvoiceItem,Product,BundleItem
# Register your models here
admin.site.register(Newinvoice),
admin.site.register(InvoiceItem),
admin.site.register(Product),
admin.site.register(BundleItem),
