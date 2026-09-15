from sqlalchemy import text

from app.database.connection import get_engine


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