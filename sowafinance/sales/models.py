from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Account
from sowaf.models import Newcustomer
# Create your models here.


class Newinvoice(models.Model):
    invoice_id = models.CharField(max_length=10, unique=True, editable=False, null=True)
    invoice_date = models.DateField(default=timezone.now)
    invoice_due = models.DateField(null=True, blank=True)
    customer = models.ForeignKey(Newcustomer, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, null=True, blank=True)
    billing_address = models.CharField(max_length=255, null=True, blank=True)
    shipping_address = models.CharField(max_length=255, null=True, blank=True)
    terms = models.CharField(max_length=255, null=True, blank=True)
    sales_rep = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    po_number = models.PositiveIntegerField(null=True, blank=True)
    item_details = models.CharField(max_length=255, null=True, blank=True)
    memo = models.CharField(max_length=255, null=True, blank=True)
    customs_notes = models.CharField(max_length=255, null=True, blank=True)
    attachments = models.FileField(null=True, blank=True)
    subtotal = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    shipping = models.FloatField(default=0)
    total_due = models.FloatField(default=0)
    class Meta:
        ordering =['invoice_date']

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            # Auto-generate next ID like 1148, 1149, etc.
            last_invoice = Newinvoice.objects.order_by('-id').first()
            next_id = 1000 if not last_invoice else int(last_invoice.invoice_id) + 1
            self.invoice_id = str(next_id)
        super().save(*args, **kwargs)


    def __str__(self):
        return f'Customer={self.customer.customer_name} | invoice date- {self.invoice_date} | Invoice due date- {self.invoice_due} | sales_representative- {self.sales_rep}'
    
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Newinvoice, on_delete=models.CASCADE, related_name='items')
    product = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    qty = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    billable = models.BooleanField(default=False)
    tax = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} x {self.qty} for Invoice {self.invoice.id}"
    


class Product(models.Model):
    PRODUCT_TYPES = [
        ('Inventory', 'Inventory'),
        ('Non-Inventory', 'Non-Inventory'),
        ('Service', 'Service'),
        ('Bundle', 'Bundle'),
    ]

    type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    class_field = models.CharField("Class", max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sell_checkbox = models.BooleanField(default=False)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # ✅ Instead of CharField, link to CoA
    income_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        limit_choices_to={'type': 'INCOME'},  # only Income accounts can be picked
        related_name="products",
        null=True, blank=True
    )

    purchase_checkbox = models.BooleanField(default=False)
    is_bundle = models.BooleanField(default=False)
    display_bundle_contents = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class BundleItem(models.Model):
    bundle = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bundle_items")
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()