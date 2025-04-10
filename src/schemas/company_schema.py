from pydantic import BaseModel, field_validator
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    city: str

    @field_validator('name')
    def validate_name(cls, value):
        if len(value) < 3 or len(value) > 50:
            raise ValueError('Name must be between 3 and 50 characters long')
        return value
    @field_validator('city')
    def validate_city(cls, value):
        if len(value) < 3 or len(value) > 50:
            raise ValueError('City must be between 3 and 50 characters long')
        return value

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None

class CompanyResponse(CompanyBase):
    id: int

    class Config:
        from_attributes = True
    
class PaginatedCompanyResponse(BaseModel):
    companies: list[CompanyResponse]
    page: int
    size: int
    total_companies: int
    total_pages: int

    class Config:
        from_attributes = True