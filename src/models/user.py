from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import db,ma,TypeDoc
from src.models.income import Income
from src.models.outgoing import Outgoing
from sqlalchemy.orm import validates
import re

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name_user = db.Column(db.String(50), nullable=False,unique=True)
    password_user = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    
    
    type_document = db.Column(db.Enum(TypeDoc),default=TypeDoc.one)
    
    balance = db.Column(db.Float,nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    incomes = db.relationship('Income', backref="owner")
    outgoings = db.relationship('Outgoing', backref="owner")
    
    def __init__(self,**fields):#Constructor, reciben muchos parametros
        super().__init__(**fields)
    
    def __repr__(self) -> str:#Similar a toString()
        return f"User >>> {self.name}"
    
    def __setattr__(self, name, value):
        if(name == "password"):
            value = User.hash_password(value)
        super(User, self).__setattr__(name, value)
    
    @staticmethod
    def hash_password(password_user):
        return generate_password_hash(password_user)
    def check_password(self, password_user):
        return check_password_hash(self.password_user, password_user)
    
    @staticmethod
    def hash_password(password_user):
        if not password_user:
            raise AssertionError('Password not provided')
        if not re.match('\d.*[A-Z]|[A-Z].*\d', password_user):
            raise AssertionError('Password must contain 1 capital letter and 1number')
        if len(password_user) < 7 or len(password_user) > 20:
            raise AssertionError('Password must be between 7 and 20 characters')
        
        return generate_password_hash(password_user)

    @validates('id')
    def validate_id(self, key, value):
        if not value:
            raise AssertionError('No id provided')
        if not re.compile("^[-+]?[0-9]+$", value):
            raise AssertionError('The value must be an integer')
        if value <= 0:
            raise AssertionError('id invalid')
        if User.query.filter(User.id == value).first():
            raise AssertionError('Id is already in use') 
        
        return value
    
    @validates('name_user')
    def validate_name_user(self,key,value):
        if not value:
            raise AssertionError('No name provided')
        if not value.isalnum():
            raise AssertionError('Name value must be alphanumeric')
        if len(value) < 5 or len(value) > 50:
            raise AssertionError('Name user must be between 5 and 50 characters')
        
        return value 
    
    @validates('password_user')
    def validate_password(self,key,value):
        if not value:
            raise AssertionError('No password provided')
        if len(value) < 5 or len(value) > 20:
            raise AssertionError('Name user must be between 5 and 20 characters')
        
        return value
    
    @validates('email')
    def validate_email(self,key,value):
        if not value:
            raise AssertionError('No email provided')
        if not re.match("[^@]+@[^@]+\.[^@]+", value):
            raise AssertionError('Provided email is not an email address')
        if User.query.filter(User.email == value).first():
            raise AssertionError('Email is already in use')
        
        return value
    
    @validates('type_document')
    def validate_type_document(self,key,value):
        if not value:
            raise AssertionError('No type_document provided')
        if value != "c.c" or value != "t.i" or value != "c.e":
            raise AssertionError('type_document invalid')
        
        return value
    
    @validates('balance')
    def validate_balance(self,key,value):
        if not value:
            raise AssertionError('No balance provided')
        return value
        
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields
        model = User
        include_fk = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)

    
