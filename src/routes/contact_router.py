from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from ..database import get_db
from ..controllers.contact_controller import get_contacts, create_contact, update_contact, delete_contact
from ..schemas.contact_schema import ContactCreate, ContactUpdate, ContactResponse, PaginatedContactResponse

router = APIRouter(prefix="/contacts", tags=["Contacts"])

@router.get("/", response_model=PaginatedContactResponse)
async def list_contacts(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    name: Optional[str] = Query(None, description="Filter by contact name"),
    company_name: Optional[str] = Query(None, description="Filter by company name")
):
    return await get_contacts(db, page, size, name, company_name)

@router.post("/", response_model=ContactResponse)
async def add_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    return await create_contact(db, contact)

@router.put("/{contact_id}", response_model=ContactResponse)
async def edit_contact(contact_id: int, contact_data: ContactUpdate, db: AsyncSession = Depends(get_db)):
    updated_contact = await update_contact(db, contact_id, contact_data)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

@router.delete("/{contact_id}")
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await delete_contact(db, contact_id)
    if contact:
        return {"message": "Contact deleted"}
    return {"error": "Contact not found"}
