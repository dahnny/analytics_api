from sqlalchemy import Column, Integer, ForeignKey, Date, Float, String, TIMESTAMP,text
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.user import User

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    image_path = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
    owner = relationship(User)  