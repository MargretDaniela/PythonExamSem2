from app.extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.Datetime, default= datetime.utcnow)
    updated_at = db.Column(db.Datetime, onupdate = datetime.utcnow)
    categories = db.relationship('Product', backref = 'categories')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __init__(self, name, categories, category_id):
        self.name = name
        self.categories = categories
        self.category_id = category_id