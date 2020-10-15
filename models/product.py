from . import db

Textes complets 
product_id
name
desc
quantity_unit
unit_price
size
color
note
trash
category_id
created_at
updated_at

# Customer Model
class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    desc = db.Column(db.Text)
    quantity_unit = db.Column(db.Integer)
    unit_price = db.Column(db.Double)
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    note = db.Column(db.Text)
    trash = db.Column(db.Boolean)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'),nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    def __init__(self, name, desc, quantity_unit, unit_price, size, color, note, trash, created_at, updated_at):
        self.name = name
        self.desc = desc
        self.quantity_unit = quantity_unit
        self.unit_price = unit_price
        self.size = size
        self.color = color
        self.note = note
        self.trash = trash
        self.address = address
        self.picture = picture
        self.credit_card = credit_card
        self.credit_card_type = credit_card_type
        self.billin_address = billin_address
        self.billing_city = billing_city
        self.billing_region = billing_region
        self.billing_postal_code = billing_postal_code
        self.remember_token = remember_token
        self.active_token = active_token
        self.online = online
        self.black_list = black_list
        self.trash = trash
        self.created_at = created_at
        self.updated_at = updated_at