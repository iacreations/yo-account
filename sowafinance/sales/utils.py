from accounts.models import Transaction, Entry, Account

def record_sale(sale):
    # Pick accounts
    sales_account = Account.objects.get(code="4000")  # Sales Revenue
    cash_account = Account.objects.get(code="1000")   # Cash
    
    # Create transaction
    txn = Transaction.objects.create(description=f"Sale to {sale.customer}")
    
    # Debit Cash
    Entry.objects.create(transaction=txn, account=cash_account, debit=sale.total_amount)
    # Credit Sales Income
    Entry.objects.create(transaction=txn, account=sales_account, credit=sale.total_amount)
