from accounts.models import Transaction, Entry, Account

def record_expense(expense):
    # Pick accounts
    expense_account = Account.objects.get(code="5000")  # Example: Office Supplies
    cash_account = Account.objects.get(code="1000")     # Cash

    # Create transaction
    txn = Transaction.objects.create(description=f"Expense: {expense.description}")

    # Debit Expense
    Entry.objects.create(transaction=txn, account=expense_account, debit=expense.amount)
    # Credit Cash
    Entry.objects.create(transaction=txn, account=cash_account, credit=expense.amount)

    return txn
