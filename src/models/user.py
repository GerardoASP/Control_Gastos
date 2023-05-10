from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import db,ma,TypeDoc
from src.models.income import Income
from src.models.outgoing import Outgoing

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name_user = db.Column(db.String(50), nullable=False,Unique=True)
    password_user = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    type_document = db.Column(db.Enum(TypeDoc),default=TypeDoc.one)
    document = db.Column(db.String(10), nullable=False)
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

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields
        model = User
        include_fk = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)

    
