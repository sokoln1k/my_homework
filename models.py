from __future__ import annotations

from typing import Any, Optional  # Добавили Any

from sqlalchemy import (
    ARRAY,
    JSON,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import RelationshipProperty, relationship, sessionmaker

# Явно указываем тип Any, чтобы mypy разрешил наследоваться от Base
Base: Any = declarative_base()


class Coffee(Base):
    # ... (код класса остается прежним)
    __tablename__ = "coffee"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    category = Column(String(200))
    description = Column(String(200))
    reviews = Column(ARRAY(String))
    user: RelationshipProperty[Optional[Users]] = relationship(
        "Users", back_populates="coffee"
    )


class Users(Base):
    # ... (код класса остается прежним)
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50))
    patronomic = Column(String(50))
    has_sale = Column(Boolean)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey("coffee.id"))
    coffee: RelationshipProperty[Optional[Coffee]] = relationship(
        "Coffee", back_populates="user"
    )


# Экспортируем engine и session, которых не хватало для app.py:
engine = create_engine(
    "postgresql+psycopg2://user:pass@localhost/dbname"
)  # укажите вашу строку подключения
Session = sessionmaker(bind=engine)
session = Session()
