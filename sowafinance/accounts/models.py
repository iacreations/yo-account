from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

class Account(models.Model):
    ACCOUNT_TYPES = [
        ("ASSET", "Asset"),
        ("LIABILITY", "Liability"),
        ("EQUITY", "Equity"),
        ("INCOME", "Income"),
        ("EXPENSE", "Expense"),
    ]
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)  # e.g. 1000 for Cash
    type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Transaction(models.Model):
    date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=255,null=True)

    def __str__(self):
        return f"{self.date} - {self.description}"

    @property
    def total_debits(self):
        return sum(entry.debit for entry in self.entries.all())

    @property
    def total_credits(self):
        return sum(entry.credit for entry in self.entries.all())


class Entry(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="entries")
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.account} | Dr {self.debit} Cr {self.credit}"

# accounts/models.py

class BankTransaction(models.Model):
    TYPE_CHOICES = [('deposit','Deposit'),('withdrawal','Withdrawal')]
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateField(auto_now_add=True)
    
class SupplierPayment(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    from_bank = models.ForeignKey('BankTransaction', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    
class Loan(models.Model):
    TYPE_CHOICES = [('disbursement','Disbursement'),('repayment','Repayment')]
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateField(auto_now_add=True)
