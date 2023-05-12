from datetime import datetime
from src.database import db,ma
from sqlalchemy.orm import validates
import re
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    income_concept = db.Column(db.String(50), nullable=False, unique=True)
    income_date = db.Column(db.DateTime,nullable=True)
    income_value = db.Column(db.Float,nullable=False)
    user_id = db.Column(db.String(10),db.ForeignKey('user.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __init__(self, **fields):
        super().__init__(**fields)
    
    def __repr__(self) -> str:
        return f"Income >>> {self.income_concept}"
    
    @validates('id')
    def validate_id(self, key, value):
        if not value:
            raise AssertionError('No id provided')
        if not re.compile("^[-+]?[0-9]+$", value):
            raise AssertionError('The value must be an integer')
        if value <= 0:
            raise AssertionError('id invalid')
        if Income.query.filter(Income.id == value).first():
            raise AssertionError('Id is already in use') 
        
        return value
    
    @validates('income_concept')
    def validate_income_concept(self,key,value):
        if not value:
            raise AssertionError('No concept provided')
        if len(value) < 5 or len(value) > 50:
            raise AssertionError('Concept must be between 5 and 50 characters')
        
        return value
    
    @validates('income_value')
    def validate_income_value(self,key,value):
        if not value:
            raise AssertionError('No value provided')
        if value < 0:
            raise AssertionError('value invalid')
        
        return value
    @validates('income_date')
    def validate_income_date(self,key,value):
        # This field is not mandatory!
        if not value:
            raise value
        if not re.match("[0-9]{1,2}\\-[0-9]{1,2}\\-[0-9]{4}", value):
            raise AssertionError('Provided date is not a real date value')
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
class IncomeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields
        model = Income
        include_fk = True

income_schema = IncomeSchema()
incomes_schema = IncomeSchema(many=True)