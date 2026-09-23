from app.database.queries import (
    get_financial_summary,
    get_invoice_count,
    get_top_expense_categories,
    get_recent_transactions,
    get_transactions,
    get_expense_category_percentage,
    get_monthly_summary,
    get_expense_by_category,
    get_income_by_category,
    get_expense_growth,
)


# ============================================================
# BASIC TOOLS
# ============================================================

def financial_summary():
    return get_financial_summary()


def invoice_count():
    return {
        "invoice_count": get_invoice_count()
    }


def top_expense_categories(limit=5):
    limit = max(1, min(int(limit), 10))
    return get_top_expense_categories(limit)


def recent_transactions(limit=5):
    limit = max(1, min(int(limit), 20))
    return get_recent_transactions(limit)


def all_transactions():
    return get_transactions()


# ============================================================
# FINANCIAL CALCULATION TOOLS
# ============================================================

def calculate_percentage(part, total):

    part = float(part)
    total = float(total)

    if total == 0:
        return {
            "part": part,
            "total": total,
            "percentage": 0.0
        }

    return {
        "part": part,
        "total": total,
        "percentage": round(
            (part / total) * 100,
            2
        )
    }


def calculate_difference(first, second):

    first = float(first)
    second = float(second)

    return {
        "first": first,
        "second": second,
        "difference": round(
            first - second,
            2
        )
    }


def calculate_ratio(first, second):

    first = float(first)
    second = float(second)

    if second == 0:
        return {
            "first": first,
            "second": second,
            "ratio": None
        }

    return {
        "first": first,
        "second": second,
        "ratio": round(
            first / second,
            4
        )
    }


def calculate_growth_rate(old_value, new_value):

    old_value = float(old_value)
    new_value = float(new_value)

    if old_value == 0:
        return {
            "old_value": old_value,
            "new_value": new_value,
            "growth_rate": None
        }

    growth_rate = (
        (new_value - old_value)
        / old_value
    ) * 100

    return {
        "old_value": old_value,
        "new_value": new_value,
        "growth_rate": round(
            growth_rate,
            2
        )
    }


# ============================================================
# EXPENSE CATEGORY PERCENTAGE
# ============================================================

def expense_category_percentage(category_name):
    return get_expense_category_percentage(
        category_name
    )


# ============================================================
# MONTHLY SUMMARY
# ============================================================

def monthly_summary(year, month):
    return get_monthly_summary(
        int(year),
        int(month)
    )


# ============================================================
# EXPENSE BY CATEGORY
# ============================================================

def expense_by_category():
    return get_expense_by_category()


# ============================================================
# INCOME BY CATEGORY
# ============================================================

def income_by_category():
    return get_income_by_category()


# ============================================================
# EXPENSE GROWTH
# ============================================================

def expense_growth(year, month):
    return get_expense_growth(
        int(year),
        int(month)
    )


# ============================================================
# PROFIT MARGIN
# ============================================================

def profit_margin():
    summary = get_financial_summary()

    income = summary["total_income"]
    profit = summary["net_profit"]

    if income == 0:
        margin = 0.0
    else:
        margin = (profit / income) * 100

    return {
        "total_income": income,
        "net_profit": profit,
        "profit_margin": round(margin, 2)
    }


# ============================================================
# INCOME / EXPENSE RATIO
# ============================================================

def income_expense_ratio():
    summary = get_financial_summary()

    income = summary["total_income"]
    expense = summary["total_expense"]

    if expense == 0:
        ratio = None
    else:
        ratio = income / expense

    return {
        "total_income": income,
        "total_expense": expense,
        "ratio": (
            round(ratio, 2)
            if ratio is not None
            else None
        )
    }