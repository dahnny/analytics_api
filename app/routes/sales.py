from app.api.deps import get_db
from app.models.user import User
from app.api.deps import get_current_user
from app.crud.sales import create_sale as create_sale_db, get_sale, get_sales, update_sale as update_sale_db, delete_sale as delete_sale_db
from app.schemas.sales import SaleCreate, SaleResponse, SaleUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/sales", tags=["sales"])

@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> SaleResponse:
    new_sale = create_sale_db(db, sale, current_user.id)
    if not new_sale:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create sale"
        )
    if current_user.id != new_sale.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create this sale"
        )
        

    return new_sale

@router.get("/{sale_id}", response_model=SaleResponse)
def read_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> SaleResponse:
    sale = get_sale(db, sale_id)
    if not sale or sale.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    return sale

@router.get("/", response_model=List[SaleResponse])
def read_sales(
    item_name: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[SaleResponse]:
    sales = get_sales(db, current_user.id, item_name)
    if not sales:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No sales found"
        )
    return sales

@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(
    sale_id: int,
    sale_update: SaleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> SaleResponse:
    sale = get_sale(db, sale_id)
    if not sale or sale.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    
    updated_sale = update_sale_db(db, sale_id, sale_update)
    if not updated_sale:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update sale"
        )
    return updated_sale

@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sale = get_sale(db, sale_id)
    if not sale or sale.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    
    if not delete_sale_db(db, sale_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete sale"
        )
    
    return {"detail": "Sale deleted successfully"}
