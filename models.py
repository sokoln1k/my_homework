from __future__ import annotations

from typing import Optional

from sqlalchemy import ARRAY, JSON, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Coffee(Base):
    __tablename__ = "coffee"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    category = Column(String(200))
    description = Column(String(200))
    reviews = Column(ARRAY(String))

    # Связь: тип оставляем, но mypy будет ругаться без stubs — это нормально
    user: Optional["Users"] = relationship("Users", back_populates="coffee")


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50))
    patronomic = Column(String(50))
    has_sale = Column(Boolean)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey("coffee.id"))

    coffee: Optional["Coffee"] = relationship("Coffee", back_populates="user")
