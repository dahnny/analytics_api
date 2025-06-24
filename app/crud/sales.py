from sqlalchemy.orm import Session
from app.models.sales import Sale
from app.schemas.sales import SaleCreate, SaleResponse, SaleUpdate
from typing import List

def create_sale(db: Session, sale: SaleCreate, user_id: int) -> Sale:
    db_sale = Sale(
        **sale.dict(), owner_id=user_id,
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sale(db: Session, sale_id: int) -> Sale | None:
    return db.query(Sale).filter(Sale.id == sale_id).first()

def get_sales(db: Session, user_id: int, item_name: str | None) -> List[Sale]:
    query = db.query(Sale).filter(Sale.owner_id == user_id)
    print(type(query)) 
    if item_name:
        query = query.filter(Sale.item.ilike(f"%{item_name}%"))
    
    return query.order_by(Sale.date.desc()).all()

def update_sale(db: Session, sale_id: int, sale_update: SaleUpdate) -> Sale | None:
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not db_sale:
        return None
    
    for key, value in sale_update.dict(exclude_unset=True).items():
        setattr(db_sale, key, value)
    
    db.commit()
    db.refresh(db_sale)
    return db_sale

def delete_sale(db: Session, sale_id: int) -> bool:
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not db_sale:
        return False
    
    db.delete(db_sale)
    db.commit()
    return True