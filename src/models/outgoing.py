from datetime import datetime
from src.database import db,ma
from sqlalchemy.orm import validates
import re

class Outgoing(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    outgoing_concept = db.Column(db.String(50), nullable=False,unique=True)
    outgoing_date = db.Column(db.Date,nullable=True)
    outgoing_value = db.Column(db.Float,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __init__(self, **fields):
        super().__init__(**fields)
    
    def __repr__(self) -> str:
        return f"Outgoing >>> {self.outgoing_concept}"
    
    @validates('id')
    def validate_id(self, key, value):
        if not value:
            raise AssertionError('No id provided')
        if not re.compile("^[-+]?[0-9]+$", value):
            raise AssertionError('The value must be an integer')
        if value <= 0:
            raise AssertionError('id invalid')
        if Outgoing.query.filter(Outgoing.id == value).first():
            raise AssertionError('Id is already in use') 
        
        return value
    
    @validates('outgoing_concept')
    def validate_outgoing_concept(self,key,value):
        if not value:
            raise AssertionError('No concept provided')
        if len(value) < 5 or len(value) > 50:
            raise AssertionError('Concept must be between 5 and 50 characters')
        if value.isdigit():
            raise AssertionError('Outgoing concept invalid')
        return value
    
    @validates('outgoing_value')
    def validate_outgoing_value(self,key,value):
        if not value:
            raise AssertionError('No value provided')
        if value < 0:
            raise AssertionError('value invalid')
        
        return value
    @validates('outgoing_date')
    def validate_outgoing_date(self,key,value):
        # This field is not mandatory!
        if not value:
            raise value
        if not re.match("[0-9]{1,2}\\-[0-9]{1,2}\\-[0-9]{4}", value):
            raise AssertionError('Provided date is not a real date value')
        today = datetime.datetime.now()
        outgoing_date = datetime.datetime.strftime(value, "%Y-%m-%d")
        if not outgoing_date >= today:
            raise AssertionError('outgoing_date date must be today or later') 
        return value
    @validates('user_id')
    def validate_user_id(self,key,value):
        if not value:
            raise AssertionError('No fk_id provided')
        if not re.compile("^[-+]?[0-9]+$", value):
            raise AssertionError('The value must be an integer')
        if value <= 0:
            raise AssertionError('fk_id invalid')
        return value
    
class OutgoingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields
        model = Outgoing
        include_fk = True

outgoing_schema = OutgoingSchema()
outgoings_schema = OutgoingSchema(many=True)