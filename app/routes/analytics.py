from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.analytics import (get_expense_breakdown, 
                                    get_financial_summary as get_financial_summary_db, 
                                    get_monthly_summary, 
                                    get_top_selling_items, get_weekly_summary)
from app.api.deps import get_db, get_current_user
from app.models.user import User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/analytics", tags=["analytics"])

# Financial Summary Endpoint
# This endpoint provides a summary of financial data including total income, expenses, and net profit.
# It allows filtering by date range.
@router.get("/summary")
def get_financial_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    
    
    try:
        start_date = datetime.fromisoformat(start_date) if start_date else None
        end_date = datetime.fromisoformat(end_date) if end_date else None
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use ISO format (YYYY-MM-DD)."
        )
    summary = get_financial_summary_db(db, current_user.id, start_date, end_date)
    
    if not summary:
        raise HTTPException(
            status_code=404,
            detail="No financial data found for the specified period."
        )
    
    return summary

# Top Selling Items Endpoint
# This endpoint retrieves the top-selling items for a user within a specified date range.
# It allows limiting the number of items returned.
@router.get("/top-selling")
def top_selling_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: str = Query(None),
    end_date: str = Query(None),
    limit: int = Query(5, ge=1, le=50),

    item: str | None = Query(None, min_length=1, max_length=100)
):
    try:
        start_date = datetime.fromisoformat(start_date) if start_date else None
        end_date = datetime.fromisoformat(end_date) if end_date else None
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use ISO format (YYYY-MM-DD)."
        )
        
    return get_top_selling_items(
        db,
        current_user.id,
        start_date,
        end_date,
        limit,
        item
    )
  
# Monthly Summary Endpoint
# This endpoint provides a monthly summary of financial data for a specific year.
# It returns total income, expenses, and net profit for each month.  
@router.get("/monthly-summary")
def monthly_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    year: int = Query(2001, ge=2000, le=2050),
    
):
    return get_monthly_summary(
        db,
        current_user.id,
        year
    )
    
@router.get("/weekly-summary")
def weekly_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    if not start_date:
        raise HTTPException(
            status_code=400,
            detail="Start date is required."
        )
    try:
        start_date = datetime.fromisoformat(start_date) if start_date else None
        end_date = datetime.fromisoformat(end_date) if end_date else None
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use ISO format (YYYY-MM-DD)."
        )

    return get_weekly_summary(
        db,
        current_user.id,
        start_date,
        end_date
    )

# Expense Breakdown Endpoint
# This endpoint provides a breakdown of expenses by category for a specific date range.
@router.get("/expense-breakdown")
def expense_breakdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    try:
        start_date = datetime.fromisoformat(start_date) if start_date else None
        end_date = datetime.fromisoformat(end_date) if end_date else None
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use ISO format (YYYY-MM-DD)."
        )

    return get_expense_breakdown(
        db,
        current_user.id,
        start_date,
        end_date
    )
    

