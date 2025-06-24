from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from typing import List


def create_expense(db: Session, expense: ExpenseCreate, user_id: int) -> Expense:
    db_expense = Expense(
        **expense.dict(), owner_id=user_id,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expense(db: Session, expense_id: int) -> Expense | None:
    return db.query(Expense).filter(Expense.id == expense_id).first()

def get_expenses(db: Session, user_id: int, item_name: str | None) -> List[Expense]:
    query = db.query(Expense).filter(Expense.owner_id == user_id)
    if item_name:
        query = query.filter(Expense.item.ilike(f"%{item_name}%"))
    
    return query.order_by(Expense.date.desc()).all()

def update_expense(db: Session, expense_id: int, expense_update: ExpenseUpdate) -> Expense | None:
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        return None
    
    for key, value in expense_update.dict(exclude_unset=True).items():
        setattr(db_expense, key, value)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int) -> bool:
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        return False
    
    db.delete(db_expense)
    db.commit()
    return True