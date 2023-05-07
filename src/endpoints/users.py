from flask import Blueprint, request
from http import HTTPStatus

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
    return {"data": user_data}, HTTPStatus.OK

@users.get("/<int:id>")
def read_one(id):
    for user in user_data:
        if user['id_user'] == id:
            return {"data": user}, HTTPStatus.OK

    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

@users.post("/")
def create():
    post_data = request.get_json()

    user = {
        "id_user": len(user_data) + 1,
        "name_user": post_data.get('name_user', 'No Name User'),
        "password_user": post_data.get('password_user', 'No password :c'),
        "email": post_data.get('email', 'No email'),
        "name": post_data.get('name', 'No Name'),
        "balance": post_data.get('balance',0.0)
    }

    user_data.append(user)

    return {"data": user}, HTTPStatus.CREATED

@users.put('/<int:id>')
@users.patch('/<int:id>')
def update(id):
    post_data = request.get_json()
    for i in range(len(user_data)):
        if user_data[i]['id_user'] == id:
            user_data[i] = {
                "id_user": id,
                "name_user": post_data.get('name_user'),
                "password_user": post_data.get('password_user'),
                "email": post_data.get('email'),
                "name": post_data.get('name'),
                "balance": post_data.get('balance')
            }
            return {"data": user_data[i]}, HTTPStatus.OK
    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

@users.delete("/<int:id>")
def delete(id):
    for i in range(len(user_data)):
        if user_data[i]['id_user'] == id:
            del user_data[i]
            return {"data": ""}, HTTPStatus.NO_CONTENT
    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND