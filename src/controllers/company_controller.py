from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from ..models.company_model import Company
from ..schemas.company_schema import CompanyCreate
import logging

from fastapi import HTTPException
import logging

async def create_company(db: AsyncSession, company: CompanyCreate):
    try:
        new_company = Company(**company.model_dump())  
        db.add(new_company)
        await db.commit()  
        await db.refresh(new_company)  
        
        return new_company 
    except Exception as e:
        logging.error(f"Error creating company: {e}") 
        raise HTTPException(status_code=500, detail="Internal server error while creating company")  


async def get_companies(db: AsyncSession, page: int = 1, size: int = 10, name: Optional[str] = None):
    offset = (page - 1) * size

    query = select(Company)

    if name:
        query = query.where(Company.name.ilike(f"%{name}%"))

    query = query.limit(size).offset(offset)

    result = await db.execute(query)
    companies = result.scalars().all()

    total_query = select(func.count(Company.id))
    if name:
        total_query = total_query.where(Company.name.ilike(f"%{name}%"))

    total_result = await db.execute(total_query)
    total_companies = total_result.scalar()

    total_pages = (total_companies + size - 1) // size  # Round up division

    return {
        "companies": companies,
        "page": page,
        "size": size,
        "total_companies": total_companies,
        "total_pages": total_pages,
    }



async def update_company(db: AsyncSession, company_id: int, company_data):
    try:
        company = await db.get(Company, company_id)
        if not company:
            return None


        for key, value in company_data.model_dump(exclude_unset=True).items():
            setattr(company, key, value)


        await db.flush()  # Ensure changes are staged
        await db.commit()
        await db.refresh(company)

        return company
    
    except Exception as e:
        await db.rollback()  
        return None


async def delete_company(db: AsyncSession, company_id: int):
    result = await db.execute(select(Company).filter(Company.id == company_id))
    company = result.scalars().first()
    if company:
        await db.delete(company)
        await db.commit()

