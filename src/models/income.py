from datetime import datetime
from src.database import db,ma

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    income_concept = db.Column(db.String(50), nullable=False,Unique=True)
    income_date = db.Column(db.DateTime,nullable=True)
    income_value = db.Column(db.Float,nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __init__(self, **fields):
        super().__init__(**fields)
    
    def __repr__(self) -> str:
        return f"Income >>> {self.income_concept}"

class IncomeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields
        model = Income
        include_fk = True

income_schema = IncomeSchema()
incomes_schema = IncomeSchema(many=True)