from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_current_user
from app.models.sales import Sale
from app.models.expense import Expense  
from datetime import datetime, timedelta
from typing import List

from app.models.user import User

def get_financial_summary(db: Session, 
                          user_id: int, 
                          start_date: datetime = None,
                          end_date: datetime = None) -> dict:
    
    sales_query = db.query(func.sum(Sale.amount)).filter(
        Sale.owner_id == user_id,       
    )
    expenses_query = db.query(func.sum(Expense.amount)).filter(
        Expense.owner_id == user_id,
    )
    
    if start_date and end_date:
        sales_query = sales_query.filter(
            Sale.date.between(start_date, end_date)
        )
        expenses_query = expenses_query.filter(
            Expense.date.between(start_date, end_date)
        )
    
    # Total income from sales
    total_income = sales_query.scalar() or 0.0
    
    # Total expenses 
    total_expenses = expenses_query.scalar() or 0.0

    net_profit = total_income - total_expenses
    
    # 
    return {
        "labels": ["Income", "Expenses", "Net Profit"],
        "datasets": [
            {
                "label": "Financial Summary",
                "data": [total_income, total_expenses, net_profit]
            }
        ]
    }

    
def get_monthly_summary(db: Session, 
                        user_id: int, 
                        year: int) -> dict:
    labels = []
    income_data = []
    expense_data = []
    profit_data = []
    
    for month in range(1, 13):
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
        
        sales_query = db.query(func.sum(Sale.amount)).filter(
            Sale.owner_id == user_id,
            Sale.date.between(start_date, end_date)
        )
            
        expenses_query = db.query(func.sum(Expense.amount)).filter(
            Expense.owner_id == user_id,
            Expense.date.between(start_date, end_date)
        )
        
        total_income = sales_query.scalar() or 0.0
        total_expenses = expenses_query.scalar() or 0.0
        
        net_profit = total_income - total_expenses
        labels.append(start_date.strftime("%b"))  # 'Jan', 'Feb', etc.
        income_data.append(total_income)
        expense_data.append(total_expenses)
        profit_data.append(net_profit)
        
    return {
        "labels": labels,
        "datasets": [
            {"label": "Income", "data": income_data},
            {"label": "Expenses", "data": expense_data},
            {"label": "Net Profit", "data": profit_data},
        ]
    }

def get_weekly_summary(db: Session, 
                       user_id: int,
                          start_date: datetime,
                          end_date: datetime | None) -> dict:
    labels = []
    income_data = []
    expense_data = []
    profit_data = []
    
    current_date = start_date
    
    # If end_date is not provided, set it to 6 days after start_date
    if not end_date:
        end_date = current_date + timedelta(days=6)

    # Ensure start_date is not later than end_date
    if start_date > end_date:
        raise ValueError("Start date cannot be later than end date.")
    
    # Ensure current_date is not later than end_date
    while current_date <= end_date:
        week_start = current_date
        # Calculate the end of the week (7 days later)
        week_end = week_start + timedelta(days=6)
        
        # query sales and expenses for the week
        sales_query = db.query(func.sum(Sale.amount)).filter(
            Sale.owner_id == user_id,
            Sale.date.between(week_start, week_end)  
        )
        expenses_query = db.query(func.sum(Expense.amount)).filter(
            Expense.owner_id == user_id,
            Expense.date.between(week_start, week_end)
        )

        total_income = sales_query.scalar() or 0.0
        total_expenses = expenses_query.scalar() or 0.0
        net_profit = total_income - total_expenses
        
        # Create chart-ready labels and data
        week_label = f"{week_start.strftime('%m/%d')}-{week_end.strftime('%m/%d')}"
        labels.append(week_label)
        income_data.append(total_income)
        expense_data.append(total_expenses)
        profit_data.append(net_profit)

        # set current_date to the next week
        current_date = week_end + timedelta(days=1)

    return {
        "labels": labels,
        "datasets": [
            {"label": "Income", "data": income_data},
            {"label": "Expenses", "data": expense_data},
            {"label": "Net Profit", "data": profit_data},
        ]
    }

def get_top_selling_items(db: Session, user_id: int, start_date: datetime | None = None, 
    end_date: datetime | None = None, limit: int = 5, item_name: str | None = None) -> dict:
    
    filters = [Sale.owner_id == user_id]

    query = db.query(
        Sale.item, 
        func.sum(Sale.quantity).label("total_quantity"), 
        func.sum(Sale.amount).label("total_revenue")
    )
    
    if start_date:
        filters.append(Sale.date >= start_date)
    if end_date:
        filters.append(Sale.date <= end_date)
    if item_name:
        filters.append(Sale.item.ilike(f"%{item_name}%"))

    query = query.filter(*filters).group_by(Sale.item).order_by(func.sum(Sale.quantity).desc()).limit(limit)

    results = query.all()
    
    # Create chart-ready data
    labels = [row.item for row in results]
    quantity_data = [row.total_quantity for row in results]
    revenue_data = [float(row.total_revenue) for row in results]

    return {
        "labels": labels,
        "datasets": [
            {"label": "Quantity Sold", "data": quantity_data},
            {"label": "Revenue (N)", "data": revenue_data},
        ]
    }
    
def get_expense_breakdown(db: Session, user_id: int, 
                          start_date: datetime | None = None, 
                          end_date: datetime | None = None) -> dict:
    
    # Query to get total expenses by category
    query = db.query(
        Expense.category,
        func.sum(Expense.amount).label("total_amount")
    ).filter(
        Expense.owner_id == user_id
    )

    # Apply date filters if provided
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)

    # Group by category and order by total amount spent
    query = query.group_by(Expense.category).order_by(func.sum(Expense.amount).desc())

    return {    
        "labels": [row.category for row in query.all()],
        "datasets": [
            {
                "label": "Total Amount",
                "data": [row.total_amount for row in query.all()]
            }
        ]
    }
