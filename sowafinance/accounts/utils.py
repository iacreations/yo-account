from accounts.models import Transaction, Entry, Account

# ----------------------------
# Sales Posting
# ----------------------------
def record_sale(sale):
    """
    Record a sale transaction:
    Debit Cash/Bank, Credit Sales Revenue
    """
    sales_account = Account.objects.get(code="4000")  # Sales Revenue
    cash_account = Account.objects.get(code="1000")   # Cash/Bank

    txn = Transaction.objects.create(description=f"Sale to {sale.customer}")

    Entry.objects.create(transaction=txn, account=cash_account, debit=sale.total_amount)
    Entry.objects.create(transaction=txn, account=sales_account, credit=sale.total_amount)

    return txn

# ----------------------------
# Expense Posting
# ----------------------------
def record_expense(expense, expense_code="5000"):
    """
    Record an expense transaction:
    Debit Expense, Credit Cash/Bank
    """
    expense_account = Account.objects.get(code=expense_code)  # Default: Office Supplies
    cash_account = Account.objects.get(code="1000")           # Cash/Bank

    txn = Transaction.objects.create(description=f"Expense: {expense.description}")

    Entry.objects.create(transaction=txn, account=expense_account, debit=expense.amount)
    Entry.objects.create(transaction=txn, account=cash_account, credit=expense.amount)

    return txn

# ----------------------------
# Bank Transactions
# ----------------------------
def record_bank_deposit(amount):
    """
    Deposit cash into bank
    Debit Bank, Credit Cash
    """
    cash_account = Account.objects.get(code="1000")
    bank_account = Account.objects.get(code="1010")

    txn = Transaction.objects.create(description="Cash deposit to bank")

    Entry.objects.create(transaction=txn, account=bank_account, debit=amount)
    Entry.objects.create(transaction=txn, account=cash_account, credit=amount)

    return txn

def record_bank_withdrawal(amount):
    """
    Withdraw from bank to cash
    Debit Cash, Credit Bank
    """
    cash_account = Account.objects.get(code="1000")
    bank_account = Account.objects.get(code="1010")

    txn = Transaction.objects.create(description="Cash withdrawal from bank")

    Entry.objects.create(transaction=txn, account=cash_account, debit=amount)
    Entry.objects.create(transaction=txn, account=bank_account, credit=amount)

    return txn

# ----------------------------
# Supplier Payments (Accounts Payable)
# ----------------------------
def record_purchase_on_credit(amount, expense_code="5000"):
    """
    Record purchase on credit
    Debit Expense, Credit Accounts Payable
    """
    expense_account = Account.objects.get(code=expense_code)
    ap_account = Account.objects.get(code="2000")  # Accounts Payable

    txn = Transaction.objects.create(description="Purchase on credit")

    Entry.objects.create(transaction=txn, account=expense_account, debit=amount)
    Entry.objects.create(transaction=txn, account=ap_account, credit=amount)

    return txn

def pay_supplier(amount, from_bank=True):
    """
    Pay supplier (settle liability)
    Debit Accounts Payable, Credit Cash/Bank
    """
    ap_account = Account.objects.get(code="2000")
    cash_or_bank = Account.objects.get(code="1010" if from_bank else "1000")

    txn = Transaction.objects.create(description="Supplier payment")

    Entry.objects.create(transaction=txn, account=ap_account, debit=amount)
    Entry.objects.create(transaction=txn, account=cash_or_bank, credit=amount)

    return txn

# ----------------------------
# Loan Transactions
# ----------------------------
def record_loan_disbursement(amount):
    """
    Record a loan received
    Debit Bank, Credit Loan Payable
    """
    bank = Account.objects.get(code="1010")
    loan = Account.objects.get(code="2200")

    txn = Transaction.objects.create(description="Loan received")

    Entry.objects.create(transaction=txn, account=bank, debit=amount)
    Entry.objects.create(transaction=txn, account=loan, credit=amount)

    return txn

def repay_loan(total_payment, principal, interest):
    """
    Repay loan with split principal & interest
    Debit Loan Payable & Interest Expense, Credit Bank
    """
    bank = Account.objects.get(code="1010")
    loan = Account.objects.get(code="2200")
    interest_exp = Account.objects.get(code="5300")  # Interest Expense

    txn = Transaction.objects.create(description="Loan repayment")

    Entry.objects.create(transaction=txn, account=loan, debit=principal)
    Entry.objects.create(transaction=txn, account=interest_exp, debit=interest)
    Entry.objects.create(transaction=txn, account=bank, credit=total_payment)

    return txn
