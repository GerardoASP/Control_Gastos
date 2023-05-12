from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug
from src.database import db
from datetime import datetime
from src.models.income import Income,income_schema,incomes_schema

incomes = Blueprint("incomes",__name__,url_prefix="/api/v1/incomes")




@incomes.get("/")
def read_all():
    incomes = Income.query.order_by(Income.income_value).all()
    return {"data": incomes_schema.dump(incomes)}, HTTPStatus.OK

@incomes.get("/<int:id>")
def read_one(id):
    income = Income.query.filter_by(id=id).first()
    if(not income):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": income_schema.dump(income)}, HTTPStatus.OK

@incomes.post("/")
def create():
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST
    income_date_request = request.get_json().get("income_date", None)
    income_datee = datetime.strptime(income_date_request, '%Y-%m-%d').date()
    # Income.id is auto increment!
    income = Income(income_concept = request.get_json().get("income_concept", None),
        income_value = request.get_json().get("income_value", None),
        income_date = income_datee,
        user_id = request.get_json().get("user_id", None))
    try:
        db.session.add(income)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"data": income_schema.dump(income)}, HTTPStatus.CREATED

@incomes.put('/<int:id>')
@incomes.patch('/<int:id>')
def update(id):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST
    income = Income.query.filter_by(id=id).first()
    if(not income):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    income_date_request = request.get_json().get("income_date", None)
    income_datee = datetime.strptime(income_date_request, '%Y-%m-%d').date()
    
    income.income_concept = request.get_json().get('income_concept', income.income_concept)
    income.income_value = request.get_json().get('income_value', income.income_value)
    income.income_date = income_datee
    income.user_id = request.get_json().get('user_id', income.user_id) 
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"data": income_schema.dump(income)}, HTTPStatus.OK

@incomes.delete("/<int:id>")
def delete(id):
    income = Income.query.filter_by(id=id).first() 
    if(not income):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    try:
        db.session.delete(income)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Resource could not be deleted","message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"data": ""}, HTTPStatus.NO_CONTENT

