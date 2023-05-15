from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug
from src.database import db
from datetime import datetime
from src.models.outgoing import Outgoing,outgoing_schema,outgoings_schema
from flask_jwt_extended import jwt_required

outgoings = Blueprint("outgoings",__name__,url_prefix="/api/v1/outgoings")



@outgoings.get("/")
@jwt_required()
def read_all():
    outgoings = Outgoing.query.order_by(Outgoing.outgoing_value).all()
    return {"data": outgoings_schema.dump(outgoings)}, HTTPStatus.OK

@outgoings.get("/<int:id>")
@jwt_required()
def read_one(id):
    outgoing = Outgoing.query.filter_by(id=id).first()
    if(not outgoing):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": outgoing_schema.dump(outgoing)}, HTTPStatus.OK

@outgoings.post("/")
@jwt_required()
def create():
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST
    outgoing_date_request = request.get_json().get("outgoing_date", None)
    outgoing_datee = datetime.strptime(outgoing_date_request, '%Y-%m-%d').date()
    # Outgoing.id is auto increment!
    outgoing = Outgoing(income_concept = request.get_json().get("Outgoing_concept", None),
        outgoing_value = request.get_json().get("outgoing_value", None),
        income_date = outgoing_datee,
        user_id = request.get_json().get("user_id", None))
    try:
        db.session.add(outgoing)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"data": outgoing_schema.dump(outgoing)}, HTTPStatus.CREATED

@outgoings.put('/<int:id>')
@outgoings.patch('/<int:id>')
@jwt_required()
def update(id):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST
    outgoing = Outgoing.query.filter_by(id=id).first()
    if(not outgoing):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    outgoing_date_request = request.get_json().get("outgoing_date", None)
    outgoing_datee = datetime.strptime(outgoing_date_request, '%Y-%m-%d').date()
    
    outgoing.outgoing_concept = request.get_json().get('outgoing_concept', outgoing.outgoing_concept)
    outgoing.outgoing_value = request.get_json().get('outgoing_value', outgoing.outgoing_value)
    outgoing.outgoing_date = outgoing_datee
    outgoing.user_id = request.get_json().get('user_id', outgoing.user_id) 
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"data": outgoing_schema.dump(outgoing)}, HTTPStatus.OK

@outgoings.delete("/<int:id>")
@jwt_required()
def delete(id):
    outgoing = Outgoing.query.filter_by(id=id).first() 
    if(not outgoing):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    try:
        db.session.delete(outgoing)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Resource could not be deleted","message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"data": ""}, HTTPStatus.NO_CONTENT