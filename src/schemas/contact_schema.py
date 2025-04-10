from pydantic import BaseModel
from typing import List, Optional

class ContactBase(BaseModel):
    name: str
    phone: str
    city: str
    company_id: int

class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    company_id: Optional[int] = None

class ContactResponse(ContactBase):
    id: int

    class Config:
        from_attributes = True

class PaginatedContactResponse(BaseModel):
    contacts: List[ContactResponse]
    page: int
    size: int
    total_contacts: int
    total_pages: int

    class Config:
        from_attributes = True
