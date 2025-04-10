from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True)
    city = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"), nullable=False)

    company = relationship("Company", back_populates="contacts")

