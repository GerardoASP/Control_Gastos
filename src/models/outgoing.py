from datetime import datetime
from src.database import db,ma

class Outgoing(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    outgoing_concept = db.Column(db.String(50), nullable=False,Unique=True)
    outgoing_date = db.Column(db.DateTime,nullable=True)
    outgoing_value = db.Column(db.Float,nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __init__(self, **fields):
        super().__init__(**fields)
    
    def __repr__(self) -> str:
        return f"Outgoing >>> {self.outgoing_concept}"

class OutgoingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields
        model = Outgoing
        include_fk = True

outgoing_schema = OutgoingSchema()
outgoings_schema = OutgoingSchema(many=True)