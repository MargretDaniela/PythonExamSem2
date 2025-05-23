from app.extensions import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer(), primary_key = True)
    first_name = db.Column(db.String(255), nullable = False)
    last_name = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.Datetime, default=datetime.now(), onupdate = datetime.utcnow)
    email = db.Column(db.String(255), nullable = False, unique = True)
    

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def full_name(self):
        return f"{self.first_name} { self.last_name}"