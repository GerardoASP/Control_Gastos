from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from enum import Enum

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()

class TypeDoc(Enum):
    one = 'c.c'
    two = 't.i'
    three = 'c.e'