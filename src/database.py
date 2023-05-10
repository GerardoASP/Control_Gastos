from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from enum import Enum

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

class TypeDoc(Enum):
    one = 'c.c'
    two = 't.i'
    three = 'c.e'