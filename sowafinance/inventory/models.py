from django.db import models
from accounts.models import Account
from sowaf.models import Newsupplier
# Create your models here.

class Product(models.Model):
    PRODUCT_TYPES = [
        ('Inventory', 'Inventory'),
        ('Non-Inventory', 'Non-Inventory'),
        ('Service', 'Service'),
        ('Bundle', 'Bundle'),
    ]
    CATEGORY_TYPES = [
        ('Good', 'Good'),
        ('Service', 'Service'),
    ]
    type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    class_field = models.CharField("Class", max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sell_checkbox = models.BooleanField(default=False)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, 
    blank=True, null=True)
    income_account = models.CharField(max_length=200,blank=True, null=True)
    expense_account = models.CharField(max_length=200,blank=True, null=True)
    supplier = models.ForeignKey(Newsupplier, on_delete=models.CASCADE,blank=True, null=True)
    purchase_checkbox = models.BooleanField(default=False)
    is_bundle = models.BooleanField(default=False)
    display_bundle_contents = models.BooleanField(default=False)

    # # ✅ Instead of CharField, link to CoA
    # income_account = models.ForeignKey(
    #     Account,
    #     on_delete=models.PROTECT,
    #     limit_choices_to={'type': 'INCOME'},  # only Income accounts can be picked
    #     related_name="products",
    #     null=True, blank=True
    # )

    # # 🔗 Link to CoA
    # income_account = models.ForeignKey(
    #     Account,
    #     on_delete=models.PROTECT,
    #     limit_choices_to={'type': 'INCOME'},
    #     related_name="income_products",
    #     null=True, blank=True
    # )
    # expense_account = models.ForeignKey(
    #     Account,
    #     on_delete=models.PROTECT,
    #     limit_choices_to={'type': 'EXPENSE'},
    #     related_name="expense_products",
    #     null=True, blank=True
    # )
    # inventory_account = models.ForeignKey(
    #     Account,
    #     on_delete=models.PROTECT,
    #     limit_choices_to={'type': 'ASSET'},
    #     related_name="asset_products",
    #     null=True, blank=True
    # )

    # def __str__(self):
    #     return self.name

class BundleItem(models.Model):
    bundle = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bundle_items")
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="used_in_bundle")
    quantity = models.PositiveIntegerField()

