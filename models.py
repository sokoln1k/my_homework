from typing import Any, Dict

import requests
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

    id = Column(Integer, Sequence("coffee_id_seq"), primary_key=True, nullable=False)
    title = Column(String(200), nullable=False)
    category = Column(String(200))
    description = Column(String(200))
    reviews = Column(ARRAY(String))
    user = relationship("Users", back_populates="coffee")

    def __repr__(self):
        return f"Товар {self.title}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("users_id_seq"), primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=True)
    patronomic = Column(String(50), nullable=True)
    has_sale = Column(Boolean)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey("coffee.id"))
    coffee = relationship("Coffee", back_populates="user")

    def __repr__(self):
        return f"Пользователь {self.name}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
