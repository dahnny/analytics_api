from app.api.deps import get_db, get_current_user
from app.models.expense import Expense
from app.crud.expense import (
    create_expense as create_expense_db,
    get_expense as get_expense_db,
    get_expenses as get_expenses_db,
    update_expense as update_expense_db,
    delete_expense as delete_expense_db
)
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User


router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ExpenseResponse:
    new_expense = create_expense_db(db, expense, current_user.id)
    if not new_expense:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create expense"
        )
    if current_user.id != new_expense.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create this expense"
        )
    
    return new_expense


@router.get("/{expense_id}", response_model=ExpenseResponse)
def read_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ExpenseResponse:
    expense = get_expense_db(db, expense_id)
    if not expense or expense.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expense

@router.get("/", response_model=List[ExpenseResponse])
def read_expenses(
    item_name: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[ExpenseResponse]:
    expenses = get_expenses_db(db, current_user.id, item_name)
    if not expenses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No expenses found"
        )
    return expenses

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ExpenseResponse:
    expense = get_expense_db(db, expense_id)
    if not expense or expense.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    updated_expense = update_expense_db(db, expense_id, expense_update)
    if not updated_expense:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update expense"
        )
    
    return updated_expense

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    expense = get_expense_db(db, expense_id)
    if not expense or expense.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    if not delete_expense_db(db, expense_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete expense"
        )
    
    return {"detail": "Expense deleted successfully"}