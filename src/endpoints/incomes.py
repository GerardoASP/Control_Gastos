from flask import Blueprint, request
from http import HTTPStatus

incomes = Blueprint("incomes",__name__,url_prefix="/api/v1/incomes")

# Data for example purposes
income_data = [
    {"id_income": 1, "income_concept": "Papitas", "income_date": "2023-05-07", "income_value": 2000},
    {"id_income": 2, "income_concept": "Gomitas", "income_date": "2023-05-07", "income_value": 2000},
    {"id_income": 3, "income_concept": "Frunas", "income_date": "2023-05-07", "income_value": 2000},
    {"id_income": 4, "income_concept": "Juguito", "income_date": "2023-05-07", "income_value": 2000},
    {"id_income": 5, "income_concept": "Galletas", "income_date": "2023-05-07", "income_value": 2000},
];


@incomes.get("/")
def read_all():
    return {"data": income_data}, HTTPStatus.OK

@incomes.get("/<int:id>")
def read_one(id):
    for income in income_data:
        if income['id_income'] == id:
            return {"data": income}, HTTPStatus.OK

    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

@incomes.post("/")
def create():
    post_data = request.get_json()

    income = {
        "id_income": len(income_data) + 1,
        "income_concept": post_data.get('income_concept', 'No Income Concept'),
        "income_date": post_data.get('income_date',None),
        "income_value": post_data.get('income_value',0)
    }

    income_data.append(income)

    return {"data": income}, HTTPStatus.CREATED

@incomes.put('/<int:id>')
@incomes.patch('/<int:id>')
def update(id):
    post_data = request.get_json()
    for i in range(len(income_data)):
        if income_data[i]['id_income'] == id:
            income_data[i] = {
                "id_income": len(income_data) + 1,
                "income_concept": post_data.get('income_concept'),
                "income_date": post_data.get('income_date'),
                "income_value": post_data.get('income_value')
            }
            return {"data": income_data[i]}, HTTPStatus.OK
    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

@incomes.delete("/<int:id>")
def delete(id):
    for i in range(len(income_data)):
        if income_data[i]['id_income'] == id:
            del income_data[i]
            return {"data": ""}, HTTPStatus.NO_CONTENT
    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
