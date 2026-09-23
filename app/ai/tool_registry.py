from app.ai.tools import (
    financial_summary,
    invoice_count,
    top_expense_categories,
    recent_transactions,
    all_transactions,

    calculate_percentage,
    calculate_difference,
    calculate_ratio,
    calculate_growth_rate,

    expense_category_percentage,
    monthly_summary,
    expense_by_category,
    income_by_category,
    expense_growth,
    profit_margin,
    income_expense_ratio,
)


TOOLS = {

    "financial_summary": financial_summary,

    "invoice_count": invoice_count,

    "top_expense_categories": top_expense_categories,

    "recent_transactions": recent_transactions,

    "all_transactions": all_transactions,

    "calculate_percentage": calculate_percentage,

    "calculate_difference": calculate_difference,

    "calculate_ratio": calculate_ratio,

    "calculate_growth_rate": calculate_growth_rate,

    "expense_category_percentage": expense_category_percentage,

    "monthly_summary": monthly_summary,

    "expense_by_category": expense_by_category,

    "income_by_category": income_by_category,

    "expense_growth": expense_growth,

    "profit_margin": profit_margin,

    "income_expense_ratio": income_expense_ratio,
}


def get_tool(tool_name):
    return TOOLS.get(tool_name)