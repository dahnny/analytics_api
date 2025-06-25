from pydantic import BaseModel
from datetime import datetime


class ExpenseBase(BaseModel):
    item: str
    amount: float
    category: str
    date: datetime
    image_path: str | None = None
    
class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True
        
class ExpenseUpdate(BaseModel):
    item: str | None = None
    amount: float | None = None
    category: str | None = None
    date: datetime | None = None
    image_path: str | None = None

    class Config:  
        orm_mode = True