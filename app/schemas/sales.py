from pydantic import BaseModel
from datetime import datetime

class SaleBase(BaseModel):
    item: str
    quantity: int 
    amount: float 
    date: datetime
    image_path: str | None = None
    
class SaleCreate(SaleBase):
    pass

class SaleResponse(SaleBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True 
        
class SaleUpdate(BaseModel):
    item: str | None = None
    quantity: int | None = None
    amount: float | None = None
    date: datetime | None = None
    image_path: str | None = None

    class Config:
        orm_mode = True
    