from __future__ import annotations
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    ARRAY,
    JSON,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Sequence,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine("postgresql+psycopg2://user:password@db:5432/skillbox_db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Coffee(Base):
    __tablename__ = "coffee"

    # Типы слева — это типы значений, которые будут в экземпляре.
    # Справа — Column(...), mypy понимает это благодаря stubs для SQLAlchemy.
    id: int = Column(Integer, Sequence("coffee_id_seq"), primary_key=True, nullable=False)
    title: str = Column(String(200), nullable=False)
    category: Optional[str] = Column(String(200))
    description: Optional[str] = Column(String(200))
    reviews: List[str] = Column(ARRAY(String))
    user: Optional["Users"] = relationship("Users", back_populates="coffee")

    def __repr__(self) -> str:
        return f"Товар {self.title}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Users(Base):
    __tablename__ = "users"

    id: int = Column(Integer, Sequence("users_id_seq"), primary_key=True)
    name: str = Column(String(50), nullable=False)
    surname: Optional[str] = Column(String(50))
    patronomic: Optional[str] = Column(String(50))
    has_sale: Optional[bool] = Column(Boolean)
    address: Optional[Dict[str, Any]] = Column(JSON)
    coffee_id: Optional[int] = Column(Integer, ForeignKey("coffee.id"))
    coffee: Optional["Coffee"] = relationship("Coffee", back_populates="user")

    def __repr__(self) -> str:
        return f"Пользователь {self.name}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
