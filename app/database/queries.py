from sqlalchemy import text
from app.database.connection import get_engine


# ============================================================
# DASHBOARD
# ============================================================

def get_financial_summary():
    engine = get_engine()

    query = text("""
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN TransactionType = 'INCOME'
                        THEN Amount
                        ELSE 0
                    END
                ), 0
            ) AS TotalIncome,

            COALESCE(
                SUM(
                    CASE
                        WHEN TransactionType = 'EXPENSE'
                        THEN Amount
                        ELSE 0
                    END
                ), 0
            ) AS TotalExpense

        FROM Transactions;
    """)

    with engine.connect() as connection:
        result = connection.execute(query).fetchone()

    total_income = float(result.TotalIncome or 0)
    total_expense = float(result.TotalExpense or 0)

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_profit": total_income - total_expense
    }


def get_invoice_count():
    engine = get_engine()

    query = text("""
        SELECT COUNT(*) AS InvoiceCount
        FROM Invoices;
    """)

    with engine.connect() as connection:
        result = connection.execute(query).fetchone()

    return int(result.InvoiceCount)


def get_top_expense_categories(limit=5):
    engine = get_engine()

    query = text("""
        SELECT TOP (:limit)
            c.CategoryName,
            SUM(t.Amount) AS TotalExpense
        FROM Transactions t
        INNER JOIN Categories c
            ON t.CategoryId = c.CategoryId
        WHERE t.TransactionType = 'EXPENSE'
        GROUP BY c.CategoryName
        ORDER BY TotalExpense DESC;
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"limit": limit}
        )

        return [
            {
                "category": row.CategoryName,
                "amount": float(row.TotalExpense)
            }
            for row in result
        ]


def get_recent_transactions(limit=5):
    engine = get_engine()

    query = text("""
        SELECT TOP (:limit)
            t.TransactionDate,
            c.CategoryName,
            t.Description,
            t.Amount,
            t.TransactionType
        FROM Transactions t
        LEFT JOIN Categories c
            ON t.CategoryId = c.CategoryId
        ORDER BY t.TransactionDate DESC, t.TransactionId DESC;
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"limit": limit}
        )

        return [
            {
                "date": row.TransactionDate,
                "category": row.CategoryName,
                "description": row.Description,
                "amount": float(row.Amount),
                "type": row.TransactionType
            }
            for row in result
        ]


def get_dashboard_data():
    summary = get_financial_summary()
    invoice_count = get_invoice_count()
    top_expenses = get_top_expense_categories()
    recent_transactions = get_recent_transactions()

    return {
        "total_income": summary["total_income"],
        "total_expense": summary["total_expense"],
        "net_profit": summary["net_profit"],
        "invoice_count": invoice_count,
        "top_expenses": top_expenses,
        "recent_transactions": recent_transactions
    }


# ============================================================
# CUSTOMERS
# ============================================================

def get_customers():
    engine = get_engine()

    query = text("""
        SELECT
            CustomerId,
            CustomerCode,
            CustomerName,
            TaxNumber,
            City,
            Phone,
            Email,
            CreatedAt
        FROM Customers
        ORDER BY CustomerName;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            {
                "id": row.CustomerId,
                "code": row.CustomerCode,
                "name": row.CustomerName,
                "tax_number": row.TaxNumber,
                "city": row.City,
                "phone": row.Phone,
                "email": row.Email,
                "created_at": row.CreatedAt
            }
            for row in result
        ]


# ============================================================
# SUPPLIERS
# ============================================================

def get_suppliers():
    engine = get_engine()

    query = text("""
        SELECT
            SupplierId,
            SupplierCode,
            SupplierName,
            TaxNumber,
            City,
            Phone,
            Email,
            CreatedAt
        FROM Suppliers
        ORDER BY SupplierName;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            {
                "id": row.SupplierId,
                "code": row.SupplierCode,
                "name": row.SupplierName,
                "tax_number": row.TaxNumber,
                "city": row.City,
                "phone": row.Phone,
                "email": row.Email,
                "created_at": row.CreatedAt
            }
            for row in result
        ]


# ============================================================
# CATEGORIES
# ============================================================

def get_categories():
    engine = get_engine()

    query = text("""
        SELECT
            CategoryId,
            CategoryName,
            CategoryType,
            CreatedAt
        FROM Categories
        ORDER BY CategoryName;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            {
                "id": row.CategoryId,
                "name": row.CategoryName,
                "type": row.CategoryType,
                "created_at": row.CreatedAt
            }
            for row in result
        ]


# ============================================================
# PRODUCTS
# ============================================================

def get_products():
    engine = get_engine()

    query = text("""
        SELECT
            p.ProductId,
            p.ProductCode,
            p.ProductName,
            p.CategoryId,
            c.CategoryName,
            p.Unit,
            p.PurchasePrice,
            p.SalePrice,
            p.StockQuantity,
            p.CreatedAt
        FROM Products p
        LEFT JOIN Categories c
            ON p.CategoryId = c.CategoryId
        ORDER BY p.ProductName;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            {
                "id": row.ProductId,
                "code": row.ProductCode,
                "name": row.ProductName,
                "category_id": row.CategoryId,
                "category": row.CategoryName,
                "unit": row.Unit,
                "purchase_price": float(row.PurchasePrice or 0),
                "sale_price": float(row.SalePrice or 0),
                "stock_quantity": float(row.StockQuantity or 0),
                "created_at": row.CreatedAt
            }
            for row in result
        ]


# ============================================================
# ACCOUNTS
# ============================================================

def get_accounts():
    engine = get_engine()

    query = text("""
        SELECT
            AccountId,
            AccountName,
            AccountType,
            AccountNumber,
            Balance,
            Currency,
            CreatedAt
        FROM Accounts
        ORDER BY AccountName;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            {
                "id": row.AccountId,
                "name": row.AccountName,
                "type": row.AccountType,
                "number": row.AccountNumber,
                "balance": float(row.Balance or 0),
                "currency": row.Currency,
                "created_at": row.CreatedAt
            }
            for row in result
        ]


# ============================================================
# INVOICES
# ============================================================

def get_invoices():
    engine = get_engine()

    query = text("""
        SELECT
            i.InvoiceId,
            i.InvoiceNumber,
            i.InvoiceDate,
            i.CustomerId,
            c.CustomerName,
            i.SupplierId,
            s.SupplierName,
            i.InvoiceType,
            i.SubTotal,
            i.TaxAmount,
            i.TotalAmount,
            i.CreatedAt
        FROM Invoices i
        LEFT JOIN Customers c
            ON i.CustomerId = c.CustomerId
        LEFT JOIN Suppliers s
            ON i.SupplierId = s.SupplierId
        ORDER BY i.InvoiceDate DESC, i.InvoiceId DESC;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            {
                "id": row.InvoiceId,
                "number": row.InvoiceNumber,
                "date": row.InvoiceDate,
                "customer_id": row.CustomerId,
                "customer": row.CustomerName,
                "supplier_id": row.SupplierId,
                "supplier": row.SupplierName,
                "type": row.InvoiceType,
                "subtotal": float(row.SubTotal or 0),
                "tax": float(row.TaxAmount or 0),
                "total": float(row.TotalAmount or 0),
                "created_at": row.CreatedAt
            }
            for row in result
        ]


# ============================================================
# INVOICE DETAILS
# ============================================================

def get_invoice_details(invoice_id):
    engine = get_engine()

    query = text("""
        SELECT
            ii.InvoiceItemId,
            ii.InvoiceId,
            ii.ProductId,
            p.ProductCode,
            p.ProductName,
            ii.Quantity,
            ii.UnitPrice,
            ii.TaxRate,
            ii.TotalAmount
        FROM InvoiceItems ii
        INNER JOIN Products p
            ON ii.ProductId = p.ProductId
        WHERE ii.InvoiceId = :invoice_id
        ORDER BY ii.InvoiceItemId;
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"invoice_id": invoice_id}
        )

        return [
            {
                "id": row.InvoiceItemId,
                "invoice_id": row.InvoiceId,
                "product_id": row.ProductId,
                "product_code": row.ProductCode,
                "product_name": row.ProductName,
                "quantity": float(row.Quantity or 0),
                "unit_price": float(row.UnitPrice or 0),
                "tax_rate": float(row.TaxRate or 0),
                "total": float(row.TotalAmount or 0)
            }
            for row in result
        ]


# ============================================================
# TRANSACTIONS
# ============================================================

def get_transactions():
    engine = get_engine()

    query = text("""
        SELECT
            t.TransactionId,
            t.TransactionDate,
            t.AccountId,
            a.AccountName,
            t.CategoryId,
            c.CategoryName,
            t.Description,
            t.Amount,
            t.TransactionType,
            t.ReferenceId,
            t.CreatedAt
        FROM Transactions t
        LEFT JOIN Accounts a
            ON t.AccountId = a.AccountId
        LEFT JOIN Categories c
            ON t.CategoryId = c.CategoryId
        ORDER BY t.TransactionDate DESC, t.TransactionId DESC;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            {
                "id": row.TransactionId,
                "date": row.TransactionDate,
                "account_id": row.AccountId,
                "account": row.AccountName,
                "category_id": row.CategoryId,
                "category": row.CategoryName,
                "description": row.Description,
                "amount": float(row.Amount or 0),
                "type": row.TransactionType,
                "reference_id": row.ReferenceId,
                "created_at": row.CreatedAt
            }
            for row in result
        ]