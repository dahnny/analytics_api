from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.analytics import get_financial_summary as get_financial_summary_db
from app.api.deps import get_db, get_current_user
from app.models.user import User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/analytics", tags=["analytics"])

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
    print(start_date, end_date, "start_date, end_date")
    summary = get_financial_summary_db(db, current_user.id, start_date, end_date)
    
    if not summary:
        raise HTTPException(
            status_code=404,
            detail="No financial data found for the specified period."
        )
    
    return summary