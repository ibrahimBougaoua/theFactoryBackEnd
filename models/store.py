from . import db

# store Model
class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    point_sale_id = db.Column(db.Integer, db.ForeignKey('point_of_sale.point_sale_id'),nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'),nullable=False)
    quantity_store = db.Column(db.Integer)
    quantity_sold = db.Column(db.Integer)

    def __init__(self, point_sale_id, product_id, quantity_store, quantity_sold):
        self.point_sale_id = point_sale_id
        self.product_id = product_id
        self.quantity_store = quantity_store
        self.quantity_sold = quantity_sold