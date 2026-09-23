from sqlalchemy import text

from app.database.connection import get_engine


# ============================================================
# FINANCIAL SUMMARY
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


# ============================================================
# INVOICE COUNT
# ============================================================

def get_invoice_count():
    engine = get_engine()

    query = text("""
        SELECT COUNT(*) AS InvoiceCount
        FROM Invoices;
    """)

    with engine.connect() as connection:
        result = connection.execute(query).fetchone()

    return int(result.InvoiceCount)


# ============================================================
# TOP EXPENSE CATEGORIES
# ============================================================
# FIX: INNER JOIN -> LEFT JOIN + COALESCE.
# Eskiden CategoryId'si NULL olan (kategorisiz) giderler bu
# sorgudan tamamen dusuyordu. Bu yuzden buradaki toplam ile
# get_financial_summary()'deki total_expense birbirini
# tutmuyordu ve model "hatali" rakamlar veriyor gibi gorunuyordu.

def get_top_expense_categories(limit=5):
    engine = get_engine()

    query = text("""
        SELECT TOP (:limit)
            COALESCE(c.CategoryName, 'Diger') AS CategoryName,
            SUM(t.Amount) AS TotalExpense

        FROM Transactions t

        LEFT JOIN Categories c
            ON t.CategoryId = c.CategoryId

        WHERE t.TransactionType = 'EXPENSE'

        GROUP BY COALESCE(c.CategoryName, 'Diger')

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


# ============================================================
# RECENT TRANSACTIONS
# ============================================================

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

        ORDER BY
            t.TransactionDate DESC,
            t.TransactionId DESC;
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


# ============================================================
# ALL TRANSACTIONS
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

        ORDER BY
            t.TransactionDate DESC,
            t.TransactionId DESC;
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


# ============================================================
# EXPENSE CATEGORY PERCENTAGE
# ============================================================

def get_expense_category_percentage(category_name):
    engine = get_engine()

    query = text("""
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN t.TransactionType = 'EXPENSE'
                        THEN t.Amount
                        ELSE 0
                    END
                ), 0
            ) AS TotalExpense,

            COALESCE(
                SUM(
                    CASE
                        WHEN t.TransactionType = 'EXPENSE'
                         AND c.CategoryName = :category_name
                        THEN t.Amount
                        ELSE 0
                    END
                ), 0
            ) AS CategoryExpense

        FROM Transactions t

        LEFT JOIN Categories c
            ON t.CategoryId = c.CategoryId;
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "category_name": category_name
            }
        ).fetchone()

    total_expense = float(result.TotalExpense or 0)
    category_expense = float(result.CategoryExpense or 0)

    if total_expense == 0:
        percentage = 0.0
    else:
        percentage = (category_expense / total_expense) * 100

    return {
        "category": category_name,
        "category_expense": round(category_expense, 2),
        "total_expense": round(total_expense, 2),
        "percentage": round(percentage, 2)
    }


# ============================================================
# MONTHLY SUMMARY
# ============================================================

def get_monthly_summary(year, month):
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

        FROM Transactions

        WHERE YEAR(TransactionDate) = :year
          AND MONTH(TransactionDate) = :month;
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "year": year,
                "month": month
            }
        ).fetchone()

    total_income = float(result.TotalIncome or 0)
    total_expense = float(result.TotalExpense or 0)

    return {
        "year": year,
        "month": month,
        "total_income": total_income,
        "total_expense": total_expense,
        "net_profit": round(total_income - total_expense, 2)
    }


# ============================================================
# EXPENSE BY CATEGORY
# ============================================================
# FIX: INNER JOIN -> LEFT JOIN + COALESCE (bkz. get_top_expense_categories)

def get_expense_by_category():
    engine = get_engine()

    query = text("""
        SELECT
            COALESCE(c.CategoryName, 'Diger') AS CategoryName,
            SUM(t.Amount) AS TotalExpense

        FROM Transactions t

        LEFT JOIN Categories c
            ON t.CategoryId = c.CategoryId

        WHERE t.TransactionType = 'EXPENSE'

        GROUP BY COALESCE(c.CategoryName, 'Diger')

        ORDER BY TotalExpense DESC;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            {
                "category": row.CategoryName,
                "amount": float(row.TotalExpense)
            }
            for row in result
        ]


# ============================================================
# INCOME BY CATEGORY
# ============================================================
# FIX: INNER JOIN -> LEFT JOIN + COALESCE (bkz. get_top_expense_categories)

def get_income_by_category():
    engine = get_engine()

    query = text("""
        SELECT
            COALESCE(c.CategoryName, 'Diger') AS CategoryName,
            SUM(t.Amount) AS TotalIncome

        FROM Transactions t

        LEFT JOIN Categories c
            ON t.CategoryId = c.CategoryId

        WHERE t.TransactionType = 'INCOME'

        GROUP BY COALESCE(c.CategoryName, 'Diger')

        ORDER BY TotalIncome DESC;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            {
                "category": row.CategoryName,
                "amount": float(row.TotalIncome)
            }
            for row in result
        ]


# ============================================================
# EXPENSE GROWTH
# ============================================================
# FIX: Eskiden iki ayri "with engine.connect()" bloguyla iki ayri
# round-trip yapiliyordu. Simdi tek sorguda, tek connection ile
# hem mevcut hem onceki ay cekiliyor. Ekstra network round-trip'i
# kaldirildigi icin bu tool daha hizli calisir.

def get_expense_growth(current_year, current_month):
    engine = get_engine()

    if current_month == 1:
        previous_year = current_year - 1
        previous_month = 12
    else:
        previous_year = current_year
        previous_month = current_month - 1

    query = text("""
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN TransactionType = 'EXPENSE'
                         AND YEAR(TransactionDate) = :current_year
                         AND MONTH(TransactionDate) = :current_month
                        THEN Amount
                        ELSE 0
                    END
                ), 0
            ) AS CurrentExpense,

            COALESCE(
                SUM(
                    CASE
                        WHEN TransactionType = 'EXPENSE'
                         AND YEAR(TransactionDate) = :previous_year
                         AND MONTH(TransactionDate) = :previous_month
                        THEN Amount
                        ELSE 0
                    END
                ), 0
            ) AS PreviousExpense

        FROM Transactions

        WHERE
            (
                YEAR(TransactionDate) = :current_year
                AND MONTH(TransactionDate) = :current_month
            )
            OR
            (
                YEAR(TransactionDate) = :previous_year
                AND MONTH(TransactionDate) = :previous_month
            );
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "current_year": current_year,
                "current_month": current_month,
                "previous_year": previous_year,
                "previous_month": previous_month
            }
        ).fetchone()

    current_expense = float(result.CurrentExpense or 0)
    previous_expense = float(result.PreviousExpense or 0)

    if previous_expense == 0:
        growth_rate = None
    else:
        growth_rate = (
            (current_expense - previous_expense)
            / previous_expense
        ) * 100

    return {
        "current_period": f"{current_year}-{current_month:02d}",
        "previous_period": f"{previous_year}-{previous_month:02d}",
        "current_expense": round(current_expense, 2),
        "previous_expense": round(previous_expense, 2),
        "growth_rate": (
            round(growth_rate, 2)
            if growth_rate is not None
            else None
        )
    }


# ============================================================
# DASHBOARD DATA
# ============================================================

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