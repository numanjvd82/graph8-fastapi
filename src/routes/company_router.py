from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from ..database import get_db
from ..schemas.company_schema import CompanyCreate, CompanyResponse, PaginatedCompanyResponse, CompanyUpdate
from ..controllers.company_controller import create_company, get_companies, delete_company, update_company

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.post("/", response_model=CompanyResponse)
async def add_company(company: CompanyCreate, db: AsyncSession = Depends(get_db)):
    return await create_company(db, company)

@router.get("/", response_model=PaginatedCompanyResponse)
async def list_companies(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    name: Optional[str] = Query(None, description="Filter by company name")
):
    return await get_companies(db, page, size, name)


@router.put("/{company_id}", response_model=CompanyResponse)
async def edit_company(company_id: int, company_data: CompanyUpdate, db: AsyncSession = Depends(get_db)):
    updated_company = await update_company(db, company_id, company_data)
    if not updated_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return updated_company

@router.delete("/{company_id}")
async def remove_company(company_id: int, db: AsyncSession = Depends(get_db)):
    await delete_company(db, company_id)
    return {"message": "Company deleted"}
