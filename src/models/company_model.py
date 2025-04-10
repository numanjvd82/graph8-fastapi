from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    city = Column(String, nullable=False)

    contacts = relationship("Contact", back_populates="company", cascade="all, delete-orphan")
