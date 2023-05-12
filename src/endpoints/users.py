from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug
from src.database import db
from src.models.user import User, user_schema, users_schema

users = Blueprint("users",__name__,url_prefix="/api/v1/users")

# Data for example purposes
user_data = [
    {"id_user": 1, "name_user": "Papitas", "password_user": "1000", "email": "d@gmail.com","name":"fer","balance":0.2},
    {"id_user": 2, "name_user": "Gomitas", "password_user": "2000", "email": "s@gmail.com","name":"fern","balance":0.3},
    {"id_user": 3, "name_user": "Frunas", "password_user": "3000", "email": "a@gmail.com","name":"ferna","balance":0.5},
    {"id_user": 4, "name_user": "Juguito", "password_user": "4000", "email": "ds@hotmail.com","name":"fed","balance":0.7},
    {"id_user": 5, "name_user": "Galletas", "password_user": "5000", "email": "dsa@hotmail.com","name":"fera","balance":0.9},
];

@users.get("/")
def read_all():
    users = User.query.order_by(User.name_user).all() 
    return {"data": users_schema.dump(users)}, HTTPStatus.OK

@users.get("/<int:id>")
def read_one(id):
    user = User.query.filter_by(id=id).first()
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": user_schema.dump(user)}, HTTPStatus.OK

@users.post("/")
def create():
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST
    # User.id is auto increment! 
    user = User(name_user = request.get_json().get("name_user", None),
        email = request.get_json().get("email", None),
        password_user = request.get_json().get("name_user", None),
        type_document = request.get_json().get("type_document", None),
        balance = request.get_json().get("balance", None))
    
    try:
        db.session.add(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST

    return {"data": user_schema.dump(user)}, HTTPStatus.CREATED

@users.put('/<int:id>')
@users.patch('/<int:id>')
def update(id):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Put body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST
    user = User.query.filter_by(id=id).first()
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    
    user.name_user = request.get_json().get('name_user', user.name_user)
    user.email = request.get_json().get('email', user.email)
    user.password_user = request.get_json().get('password_user', user.password_user)
    user.balance = request.get_json().get('balance', user.balance)
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"data": user_schema.dump(user)}, HTTPStatus.OK

@users.delete("/<int:id>")
def delete(id):
    user = User.query.filter_by(id=id).first()
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    try:
        db.session.delete(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Resource could not be deleted","message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"data": ""}, HTTPStatus.NO_CONTENT
