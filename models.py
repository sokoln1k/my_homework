import requests
from sqlalchemy import Column, Integer, String, Boolean, JSON, ARRAY, Sequence, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from typing import Dict, Any

engine = create_engine('postgresql+psycopg2://user:password@db:5432/skillbox_db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Coffee(Base):
    __tablename__ = 'coffee'

    id = Column(Integer, Sequence('coffee_id_seq'), primary_key=True, nullable=False)
    title = Column(String(200), nullable=False)
    category = Column(String(200))
    description = Column(String(200))
    reviews = Column(ARRAY(String))
    user = relationship("Users", back_populates="coffee")

    def __repr__(self):
        return f"Товар {self.title}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('users_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=True)
    patronomic = Column(String(50), nullable=True)
    has_sale = Column(Boolean)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey('coffee.id'))
    coffee = relationship('Coffee', back_populates='user')

    def __repr__(self):
        return f"Пользователь {self.name}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}




# def before_first_request():
#     Base.metadata.create_all(engine)
#     if not session.query(Users).all():
#         users_data = requests.get("https://dummyjson.com/users", params={"limit": 10}).json()['users']
#         users_name = [user['firstName'] for user in users_data]
#         users_address = [user['address'] for user in users_data]
#
#         coffee_data = requests.get("https://dummyjson.com/products/search", params={"limit": 10, 'q': 'coffee'}).json()["products"][0]
#         coffee_objects = {
#                 "title": coffee_data["title"],
#                 "category": coffee_data["category"],
#                 "description": coffee_data["description"],
#                 "reviews": [comment['comment'] for comment in coffee_data["reviews"]]
#         }
#
#         objects = [
#             Coffee(**coffee_objects),
#             Users(name=users_name[0], has_sale=True, address=users_address[0], coffee_id=1),
#             Users(name=users_name[1], has_sale=False, address=users_address[1], coffee_id=1),
#             Users(name=users_name[2], has_sale=True, address=users_address[2], coffee_id=1),
#             Users(name=users_name[3], has_sale=False, address=users_address[3], coffee_id=1),
#             Users(name=users_name[4], has_sale=True, address=users_address[4], coffee_id=1),
#             Users(name=users_name[5], has_sale=False, address=users_address[5], coffee_id=1),
#             Users(name=users_name[6], has_sale=True, address=users_address[6], coffee_id=1),
#             Users(name=users_name[7], has_sale=False, address=users_address[7], coffee_id=1),
#             Users(name=users_name[8], has_sale=True, address=users_address[8], coffee_id=1),
#             Users(name=users_name[9], has_sale=False, address=users_address[9], coffee_id=1)
#         ]
#
#         session.bulk_save_objects(objects)
#         session.commit()



