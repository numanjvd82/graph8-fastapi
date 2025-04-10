from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Optional
from ..models.contact_model import Contact
from ..models.company_model import Company

async def get_contacts(db: AsyncSession, page: int = 1, size: int = 10, name: Optional[str] = None, company_name: Optional[str] = None):
    offset = (page - 1) * size

    query = select(Contact).join(Company)

    if name:
        query = query.where(Contact.name.ilike(f"%{name}%"))
    if company_name:
        query = query.where(Company.name.ilike(f"%{company_name}%"))

    query = query.limit(size).offset(offset)
    result = await db.execute(query)
    contacts = result.scalars().all()

    # Count total contacts
    total_query = select(func.count(Contact.id)).join(Company)
    if name:
        total_query = total_query.where(Contact.name.ilike(f"%{name}%"))
    if company_name:
        total_query = total_query.where(Company.name.ilike(f"%{company_name}%"))

    total_result = await db.execute(total_query)
    total_contacts = total_result.scalar()

    total_pages = (total_contacts + size - 1) // size

    return {
        "contacts": contacts,
        "page": page,
        "size": size,
        "total_contacts": total_contacts,
        "total_pages": total_pages,
    }

async def create_contact(db: AsyncSession, contact_data):
    new_contact = Contact(**contact_data.model_dump())
    db.add(new_contact)
    await db.commit()
    await db.refresh(new_contact)
    return new_contact

async def update_contact(db: AsyncSession, contact_id: int, contact_data):
    contact = await db.get(Contact, contact_id)
    if not contact:
        return None

    for key, value in contact_data.model_dump(exclude_unset=True).items():
        setattr(contact, key, value)

    await db.commit()
    await db.refresh(contact)
    return contact

async def delete_contact(db: AsyncSession, contact_id: int):
    contact = await db.get(Contact, contact_id)
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
