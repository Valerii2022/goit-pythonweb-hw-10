from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate
from typing import List

class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def create_contact(self, contact: ContactCreate):
        return await self.repository.create_contact(contact)

    async def get_contacts(self, skip: int, limit: int) -> List:
        return await self.repository.get_contacts(skip, limit)

    async def get_contact_by_id(self, contact_id: int):
        return await self.repository.get_contact_by_id(contact_id)

    async def get_contacts_by_name(self, name: str, skip: int, limit: int) -> List:
        return await self.repository.get_contacts_by_name(name, skip, limit)

    async def update_contact(self, contact_id: int, contact_data: ContactUpdate):
        return await self.repository.update_contact(contact_id, contact_data)

    async def delete_contact(self, contact_id: int):
        return await self.repository.delete_contact(contact_id)

