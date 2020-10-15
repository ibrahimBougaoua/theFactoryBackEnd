from . import db

# Customer Sales Model
class CustomerSales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'),nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.payment_id'),nullable=False)
    point_sale_id = db.Column(db.Integer, db.ForeignKey('point_of_sale.point_sale_id'),nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'),nullable=False)
    quantity = db.Column(db.Integer)
    paid = db.Column(db.Boolean)
    payment_date = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP)

    def __init__(self, customer_id, payment_id, point_sale_id, product_id, quantity, paid, payment_date ,created_at):
        self.customer_id = customer_id
        self.payment_id = payment_id
        self.point_sale_id = point_sale_id
        self.product_id = product_id
        self.quantity = quantity
        self.paid = paid
        self.payment_date = payment_date
        self.created_at = created_at