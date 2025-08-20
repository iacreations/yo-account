from django.db import models
from django.utils import timezone


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('ASSET', 'Asset'),
        ('LIABILITY', 'Liability'),
        ('EQUITY', 'Equity'),
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]

    code = models.CharField(max_length=20, unique=True)  # e.g. 1000, 2000
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Transaction(models.Model):
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    reference = models.CharField(max_length=50, blank=True, null=True)  # e.g. invoice_id
    posted = models.BooleanField(default=False)  # track if locked/posted

    def __str__(self):
        return f"Txn {self.id} - {self.date}"


class TransactionLine(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="lines")
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.account.name}: Dr {self.debit} | Cr {self.credit}"

