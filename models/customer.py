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
    online = db.Column(db.Boolean, default=False, server_default="false")
    black_list = db.Column(db.Boolean, default=False, server_default="false")
    trash = db.Column(db.Boolean, default=False, server_default="false")
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