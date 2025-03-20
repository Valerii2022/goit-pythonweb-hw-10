from typing import List, Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate
from sqlalchemy.sql import extract

class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, skip: int, limit: int) -> List[Contact]:
        stmt = select(Contact).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        stmt = select(Contact).filter(Contact.id == contact_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_contacts_by_name(self, name: str, skip: int, limit: int) -> List[Contact]:
        stmt = select(Contact).filter(Contact.first_name.ilike(f"%{name}%")).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create_contact(self, body: ContactCreate) -> Contact:
        db_contact = Contact(
            first_name=body.first_name,
            last_name=body.last_name,
            email=body.email,
            phone=body.phone,
            birth_date=body.birth_date,
            additional_info=body.additional_info,
        )
        self.db.add(db_contact)
        await self.db.commit()
        await self.db.refresh(db_contact)
        return db_contact

    async def update_contact(self, contact_id: int, body: ContactUpdate) -> Optional[Contact]:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            if body.first_name:
                contact.first_name = body.first_name
            if body.last_name:
                contact.last_name = body.last_name
            if body.email:
                contact.email = body.email
            if body.phone:
                contact.phone = body.phone
            if body.birth_date:
                contact.birth_date = body.birth_date
            if body.additional_info:
                contact.additional_info = body.additional_info
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def delete_contact(self, contact_id: int) -> Optional[Contact]:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact
    
    async def search_contacts(self, name: Optional[str], surname: Optional[str], email: Optional[str]):
        stmt = select(Contact)
        if name:
            stmt = stmt.where(Contact.first_name.ilike(f"%{name}%"))
        if surname:
            stmt = stmt.where(Contact.last_name.ilike(f"%{surname}%"))
        if email:
            stmt = stmt.where(Contact.email.ilike(f"%{email}%"))
        
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_upcoming_birthdays(self, today: date, next_week: date):
        stmt = select(Contact).where(
            extract('month', Contact.birth_date) == today.month,
            extract('day', Contact.birth_date) >= today.day,
        ).where(
            (extract('month', Contact.birth_date) == next_week.month) &
            (extract('day', Contact.birth_date) <= next_week.day)
        )
    
        result = await self.db.execute(stmt)
        return result.scalars().all()

