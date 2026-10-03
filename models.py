from __future__ import annotations
from typing import Dict, Any, List

from sqlalchemy import Column, Integer, String, Boolean, JSON, ARRAY, Sequence, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

engine = create_engine("postgresql+psycopg2://user:password@db:5432/skillbox_db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Coffee(Base):
    __tablename__ = "coffee"

    id: int = Column(Integer, Sequence("coffee_id_seq"), primary_key=True, nullable=False)
    title: str = Column(String(200), nullable=False)
    category: str | None = Column(String(200))
    description: str | None = Column(String(200))
    reviews: List[str] = Column(ARRAY(String))
    user: Users | None = relationship("Users", back_populates="coffee")

    def __repr__(self) -> str:
        return f"Товар {self.title}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Users(Base):
    __tablename__ = "users"

    id: int = Column(Integer, Sequence("users_id_seq"), primary_key=True)
    name: str = Column(String(50), nullable=False)
    surname: str | None = Column(String(50))
    patronomic: str | None = Column(String(50))
    has_sale: bool | None = Column(Boolean)
    address: dict[str, Any] | None = Column(JSON)
    coffee_id: int | None = Column(Integer, ForeignKey("coffee.id"))
    coffee: Coffee | None = relationship("Coffee", back_populates="user")

    def __repr__(self) -> str:
        return f"Пользователь {self.name}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
