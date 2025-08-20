from django.db import migrations

def create_coa(apps, schema_editor):
    Account = apps.get_model('accounts', 'Account')
    starter_accounts = [
        # Assets
        {"code": "1000", "name": "Cash", "type": "ASSET"},
        {"code": "1010", "name": "Bank Account", "type": "ASSET"},
        {"code": "1100", "name": "Accounts Receivable", "type": "ASSET"},
        {"code": "1200", "name": "Inventory", "type": "ASSET"},
        {"code": "1300", "name": "Prepaid Expenses", "type": "ASSET"},
        {"code": "1400", "name": "Office Equipment", "type": "ASSET"},
        {"code": "1410", "name": "Accumulated Depreciation", "type": "ASSET"},
        {"code": "1500", "name": "Vehicles", "type": "ASSET"},
        {"code": "1510", "name": "Land & Buildings", "type": "ASSET"},

        # Liabilities
        {"code": "2000", "name": "Accounts Payable", "type": "LIABILITY"},
        {"code": "2100", "name": "Accrued Expenses", "type": "LIABILITY"},
        {"code": "2200", "name": "Wages Payable", "type": "LIABILITY"},
        {"code": "2300", "name": "Taxes Payable (VAT)", "type": "LIABILITY"},
        {"code": "2400", "name": "Short-term Loan", "type": "LIABILITY"},
        {"code": "2500", "name": "Long-term Loan", "type": "LIABILITY"},

        # Equity
        {"code": "3000", "name": "Owner’s Equity", "type": "EQUITY"},
        {"code": "3100", "name": "Retained Earnings", "type": "EQUITY"},
        {"code": "3200", "name": "Owner’s Drawings", "type": "EQUITY"},

        # Income
        {"code": "4000", "name": "Sales Income", "type": "INCOME"},
        {"code": "4100", "name": "Service Income", "type": "INCOME"},
        {"code": "4200", "name": "Interest Income", "type": "INCOME"},
        {"code": "4300", "name": "Other Income", "type": "INCOME"},

        # Expenses
        {"code": "5000", "name": "Cost of Goods Sold (COGS)", "type": "EXPENSE"},
        {"code": "5100", "name": "Rent Expense", "type": "EXPENSE"},
        {"code": "5200", "name": "Salaries Expense", "type": "EXPENSE"},
        {"code": "5210", "name": "Wages Expense", "type": "EXPENSE"},
        {"code": "5300", "name": "Utilities Expense", "type": "EXPENSE"},
        {"code": "5400", "name": "Office Supplies", "type": "EXPENSE"},
        {"code": "5500", "name": "Marketing Expense", "type": "EXPENSE"},
        {"code": "5600", "name": "Travel Expense", "type": "EXPENSE"},
        {"code": "5700", "name": "Depreciation Expense", "type": "EXPENSE"},
        {"code": "5800", "name": "Professional Fees", "type": "EXPENSE"},
        {"code": "5900", "name": "Bank Charges", "type": "EXPENSE"},
    ]

    for acc in starter_accounts:
        Account.objects.get_or_create(code=acc["code"], defaults=acc)

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),  # replace with your last migration
    ]

    operations = [
        migrations.RunPython(create_coa),
    ]
