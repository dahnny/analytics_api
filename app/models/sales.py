from sqlalchemy import Column, Integer, ForeignKey, Date, Float, String, TIMESTAMP,text
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.user import User

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    quantity = Column(Integer, default=1)
    date = Column(Date, nullable=False)
    image_path = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, server_default=text("now()"))
    
    owner = relationship(User)