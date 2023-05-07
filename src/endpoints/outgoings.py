from flask import Blueprint, request
from http import HTTPStatus

outgoings = Blueprint("outgoings",__name__,url_prefix="/api/v1/outgoings")

# Data for example purposes
outgoing_data = [
    {"id_outgoing": 1, "outgoing_concept": "Papitas", "outgoing_date": "2023-05-07", "outgoing_value": 2000},
    {"id_outgoing": 2, "outgoing_concept": "Gomitas", "outgoing_date": "2023-05-07", "outgoing_value": 2000},
    {"id_outgoing": 3, "outgoing_concept": "Frunas", "outgoing_date": "2023-05-07", "outgoing_value": 2000},
    {"id_outgoing": 4, "outgoing_concept": "Juguito", "outgoing_date": "2023-05-07", "outgoing_value": 2000},
    {"id_outgoing": 5, "outgoing_concept": "Galletas", "outgoing_date": "2023-05-07", "outgoing_value": 2000},
];

@outgoings.get("/")
def read_all():
    return {"data": outgoing_data}, HTTPStatus.OK

@outgoings.get("/<int:id>")
def read_one(id):
    for outgoing in outgoing_data:
        if outgoing['id_outgoing'] == id:
            return {"data": outgoing}, HTTPStatus.OK

    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

@outgoings.post("/")
def create():
    post_data = request.get_json()

    outgoing = {
        "id_outgoing": len(outgoing_data) + 1,
        "outgoing_concept": post_data.get('outgoing_concept', 'No outgoing Concept'),
        "outgoing_date": post_data.get('outgoing_date',None),
        "outgoing_value": post_data.get('outgoing_value',0)
    }

    outgoing_data.append(outgoing)

    return {"data": outgoing}, HTTPStatus.CREATED

@outgoings.put('/<int:id>')
@outgoings.patch('/<int:id>')
def update(id):
    post_data = request.get_json()
    for i in range(len(outgoing_data)):
        if outgoing_data[i]['id_outgoing'] == id:
            outgoing_data[i] = {
                "id_outgoing": len(outgoing_data) + 1,
                "outgoing_concept": post_data.get('outgoing_concept'),
                "outgoing_date": post_data.get('outgoing_date'),
                "outgoing_value": post_data.get('outgoing_value')
            }
            return {"data": outgoing_data[i]}, HTTPStatus.OK
    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

@outgoings.delete("/<int:id>")
def delete(id):
    for i in range(len(outgoing_data)):
        if outgoing_data[i]['id_outgoing'] == id:
            del outgoing_data[i]
            return {"data": ""}, HTTPStatus.NO_CONTENT
    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND