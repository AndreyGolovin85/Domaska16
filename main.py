import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from db_init import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datebase.db"
app.config["JSON_AS_ASCII"] = False
db = SQLAlchemy(app)


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return json.dumps([user.to_dict() for user in User.query.all()])
    if request.method == "POST":
        user = json.loads(request.data)
        add_new_user = User(
            id=user["id"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            age=user["age"],
            email=user["email"],
            role=user["role"],
            phone=user["phone"]
        )
        db.session.add(add_new_user)
        db.session.commit()
        db.session.close()
        return "Пользователь добавлен в базу"


@app.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def one_user(user_id):
    if request.method == "GET":
        user = User.query.get(user_id)
        if user is None:
            return "Такого пользователя не найдено"
        return json.dumps(user.to_dict())
    elif request.method == "PUT":
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Такого пользователя не найдено"
        user.id = user_data["id"],
        user.first_name = user_data["first_name"],
        user.last_name = user_data["last_name"],
        user.age = user_data["age"],
        user.email = user_data["email"],
        user.role = user_data["role"],
        user.phone = user_data["phone"]
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return f"Пользователь с id {user_id} успешно изменён!"
    elif request.method == "DELETE":
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Такого пользователя не найдено"
        db.session.delete(user)
        db.session.commit()
        db.session.close()
        return f"Пользователь с id {user_id} успешно удален!"


@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        return jsonify([order.to_dict() for order in Order.query.all()])
    if request.method == "POST":
        order = json.loads(request.data)
        add_new_order = Order(
            id=order["id"],
            name=order["name"],
            description=order["description"],
            start_date=datetime.date(year=y_start, month=m_start, day=d_start),
            end_data=datetime.date(year=y_end, month=m_end, day=d_end),
            address=order["address"],
            price=order["price"],
            customer_id=order["customer_id"],
            executor_id=order["executor_id"]
        )
        db.session.add(add_new_order)
        db.session.commit()
        db.session.close()
        return "Заказ добавлен в базу"


@app.route("/orders/<int:order_id>", methods=["GET", "PUT", "DELETE"])
def one_order(order_id):
    if request.method == "GET":
        order = Order.query.get(order_id)
        if order is None:
            return "Нет такого заказа"
        return jsonify(order.to_dict())
    elif request.method == "PUT":
        order_data = json.loads(request.data)
        order = db.session.query(Order).get(order_id)
        if order is None:
            return "Такого пользователя не найдено"
        order.id = order_data["id"],
        order.name = order_data["name"],
        order.description = order_data["description"],
        order.start_date = datetime.date(year=y_start, month=m_start, day=d_start),
        order.end_data = datetime.date(year=y_end, month=m_end, day=d_end),
        order.address = order_data["address"],
        order.price = order_data["price"],
        order.customer_id = order_data["customer_id"],
        order.executor_id = order_data["executor_id"]
        db.session.add(order)
        db.session.commit()
        db.session.close()
        return f"Заказ с id {order_id} успешно изменён!"
    elif request.method == "DELETE":
        order = db.session.query(User).get(order_id)
        if order is None:
            return "Такого заказа не найдено"
        db.session.delete(order)
        db.session.commit()
        db.session.close()
        return f"Заказ с id {order_id} успешно удален!"


@app.route("/offers", methods=["GET", "POST"])
def offers():
    if request.method == "GET":
        return json.dumps([offer.to_dict() for offer in Offer.query.all()])
    if request.method == "POST":
        offer = json.loads(request.data)
        add_new_offer = Offer(
            id=offer["id"],
            order_id=offer["order_id"],
            executor_id=offer["executor_id"]
        )
        db.session.add(add_new_offer)
        db.session.commit()
        db.session.close()
        return "Предложение добавлено в базу"


@app.route("/offers/<int:offer_id>", methods=["GET", "PUT", "DELETE"])
def one_offer(offer_id):
    if request.method == "GET":
        offer = Offer.query.get(offer_id)
        if offer is None:
            return "Нет такого заказа"
        return json.dumps(offer.to_dict())
    elif request.method == "PUT":
        offer_data = json.loads(request.data)
        offer = db.session.query(Offer).get(offer_id)
        if offer is None:
            return "Такого заказа не найдено"
        offer.id = offer_data["id"],
        offer.order_id = offer_data["order_id"],
        offer.executor_id = offer_data["executor_id"]
        db.session.add(offer)
        db.session.commit()
        db.session.close()
        return f"Заказ с id {offer_id} успешно изменён!"
    elif request.method == "DELETE":
        offer = db.session.query(User).get(offer_id)
        if offer is None:
            return "Такого заказа не найдено"
        db.session.delete(offer)
        db.session.commit()
        db.session.close()
        return f"Заказ с id {offer_id} успешно удален!"


if __name__ == "__main__":
    app.run(port=3070)
