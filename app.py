import requests
from flask import Flask, jsonify, request
from sqlalchemy import func, select
from sqlalchemy.sql import Select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError

from models import Base, Coffee, Users, engine, session
from schemas import UserCreate

app = Flask(__name__)


@app.before_request
def before_first_request():
    Base.metadata.create_all(engine)
    if not session.query(Users).all():
        users_data = requests.get(
            "https://dummyjson.com/users", params={"limit": 10}
        ).json()["users"]
        users_name = [user["firstName"] for user in users_data]
        users_address = [user["address"] for user in users_data]

        coffee_data = requests.get(
            "https://dummyjson.com/products/search", params={"limit": 10, "q": "coffee"}
        ).json()["products"][0]
        coffee_objects = {
            "title": coffee_data["title"],
            "category": coffee_data["category"],
            "description": coffee_data["description"],
            "reviews": [comment["comment"] for comment in coffee_data["reviews"]],
        }

        objects = [
            Coffee(**coffee_objects),
            Users(
                name=users_name[0], has_sale=True, address=users_address[0], coffee_id=1
            ),
            Users(
                name=users_name[1],
                has_sale=False,
                address=users_address[1],
                coffee_id=1,
            ),
            Users(
                name=users_name[2], has_sale=True, address=users_address[2], coffee_id=1
            ),
            Users(
                name=users_name[3],
                has_sale=False,
                address=users_address[3],
                coffee_id=1,
            ),
            Users(
                name=users_name[4], has_sale=True, address=users_address[4], coffee_id=1
            ),
            Users(
                name=users_name[5],
                has_sale=False,
                address=users_address[5],
                coffee_id=1,
            ),
            Users(
                name=users_name[6], has_sale=True, address=users_address[6], coffee_id=1
            ),
            Users(
                name=users_name[7],
                has_sale=False,
                address=users_address[7],
                coffee_id=1,
            ),
            Users(
                name=users_name[8], has_sale=True, address=users_address[8], coffee_id=1
            ),
            Users(
                name=users_name[9],
                has_sale=False,
                address=users_address[9],
                coffee_id=1,
            ),
        ]

        session.bulk_save_objects(objects)
        session.commit()


@app.route("/add/user", methods=["POST"])
def get_new_user():
    try:
        new_user = UserCreate(**request.json)

    except Exception as e:
        return jsonify({"error": "Validation error", "details": str(e)}), 400

    try:
        insert_query = insert(Users).values(
            name=new_user.name,
            has_sale=new_user.has_sale,
            address=new_user.address,
            coffee_id=new_user.coffee_id,
        )
        session.execute(insert_query)
        session.commit()

        new_user_coffee = (
            session.query(Coffee.title).where(Coffee.id == new_user.coffee_id).scalar()
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "new_user": new_user.name,
                    "coffee_prefer": new_user_coffee,
                }
            ),
            200,
        )

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500


@app.route("/search/coffee/<string:title>", methods=["GET"])
def search_coffee_for_title(title: str):
    ts_query = func.plainto_tsquery("russian", title)

    stmt: Select[tuple[str]] = select(Coffee.title).where(Coffee.title.op("@@")(ts_query))

    results = session.execute(stmt).scalars().first()

    if not results:
        return jsonify({"error": "Данный кофе не найден в базе данных"}), 404

    return jsonify({"title": results})


@app.route("/reviews/unique", methods=["GET"])
def search_unique_reviews_for_coffee():
    stmt: Select[tuple[str]] = select(func.unnest(Coffee.reviews)).distinct()
    unique_reviews = session.execute(stmt).scalars().all()
    if not unique_reviews:
        return jsonify({"error": "Нет уникальных заметок"})
    return jsonify({"unique_reviews": unique_reviews})
