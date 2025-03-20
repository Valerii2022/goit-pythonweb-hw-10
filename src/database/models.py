from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import  DeclarativeBase
from sqlalchemy.sql.sqltypes import Date

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    birth_date = Column(Date, nullable=False)
    additional_info = Column(String, nullable=True)



