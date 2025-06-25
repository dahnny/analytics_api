from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.sales import Sale
from app.models.expense import Expense  
from datetime import datetime

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

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_profit": net_profit
    }   