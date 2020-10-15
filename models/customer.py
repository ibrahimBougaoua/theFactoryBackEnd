from . import db

# Customer Model
class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    phone = db.Column(db.String(15))
    city = db.Column(db.String(20))
    address = db.Column(db.Text)
    picture = db.Column(db.String(50))
    credit_card = db.Column(db.String(100))
    credit_card_type = db.Column(db.String(100))
    billin_address = db.Column(db.String(100))
    billing_city = db.Column(db.String(100))
    billing_region = db.Column(db.String(100))
    billing_postal_code = db.Column(db.String(100))
    remember_token = db.Column(db.String(100))
    active_token = db.Column(db.String(100))
    online = db.Column(db.Boolean)
    black_list = db.Column(db.Boolean)
    trash = db.Column(db.Boolean)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    def __init__(self, first_name, last_name, email, password, gender, age, phone, city, address, picture, credit_card ,credit_card_type ,billin_address ,billing_city ,billing_region ,billing_postal_code, remember_token, active_token,online, black_list, trash, created_at, updated_at):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.gender = gender
        self.age = age
        self.phone = phone
        self.city = city
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

# Customer Sales Model
class CustomerSales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'),nullable=False)
    payment_id = db.Column(db.Integer)#db.Column(db.Integer, db.ForeignKey('payment.payment_id'),nullable=False)
    point_sale_id = db.Column(db.Integer)#db.Column(db.Integer, db.ForeignKey('point_of_sale.point_sale_id'),nullable=False)
    product_id = db.Column(db.Integer)#db.Column(db.Integer, db.ForeignKey('product.product_id'),nullable=False)
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