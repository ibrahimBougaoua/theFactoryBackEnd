from . import db

# Product Model
class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    desc = db.Column(db.Text)
    quantity_unit = db.Column(db.Integer)
    unit_price = db.Column(db.Integer)
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    note = db.Column(db.Text)
    trash = db.Column(db.Boolean, default=False, server_default="false")
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'),nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    def __init__(self, name, desc, quantity_unit, unit_price, size, color, note, trash, category_id, created_at, updated_at):
        self.name = name
        self.desc = desc
        self.quantity_unit = quantity_unit
        self.unit_price = unit_price
        self.size = size
        self.color = color
        self.note = note
        self.trash = trash
        self.category_id = category_id
        self.created_at = created_at
        self.updated_at = updated_at