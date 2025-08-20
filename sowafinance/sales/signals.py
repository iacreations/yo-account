# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from sales.models import Newinvoice
from expenses.models import Expense
from accounts.models import BankTransaction, SupplierPayment, Loan
from accounts.utils import (
    record_sale,
    record_expense,
    record_bank_deposit,
    record_bank_withdrawal,
    pay_supplier,
    record_loan_disbursement,
    repay_loan
)

# ----------------------------
# Sales Signal
# ----------------------------
@receiver(post_save, sender=Newinvoice)
def auto_post_sale(sender, instance, created, **kwargs):
    if created:
        record_sale(instance)

# ----------------------------
# Expenses Signal
# ----------------------------
@receiver(post_save, sender=Expense)
def auto_post_expense(sender, instance, created, **kwargs):
    if created:
        record_expense(instance)

# ----------------------------
# Bank Transactions Signal
# ----------------------------
@receiver(post_save, sender=BankTransaction)
def auto_post_bank(sender, instance, created, **kwargs):
    if created:
        if instance.type == "deposit":
            record_bank_deposit(instance.amount)
        elif instance.type == "withdrawal":
            record_bank_withdrawal(instance.amount)

# ----------------------------
# Supplier Payments Signal
# ----------------------------
@receiver(post_save, sender=SupplierPayment)
def auto_post_supplier(sender, instance, created, **kwargs):
    if created:
        pay_supplier(instance.amount, from_bank=instance.from_bank)

# ----------------------------
# Loan Transactions Signal
# ----------------------------
@receiver(post_save, sender=Loan)
def auto_post_loan(sender, instance, created, **kwargs):
    if created:
        if instance.type == "disbursement":
            record_loan_disbursement(instance.amount)
        elif instance.type == "repayment":
            repay_loan(instance.total_payment, instance.principal, instance.interest)
