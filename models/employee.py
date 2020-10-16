from . import db

# Employee Model
class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key = True)
    manage_id = db.Column(db.Integer)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(15))
    city = db.Column(db.String(20))
    address = db.Column(db.Text)
    picture = db.Column(db.String(50))
    enable = db.Column(db.Boolean)
    remember_token = db.Column(db.String(100))
    trash = db.Column(db.Boolean)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    def __init__(self, manage_id, first_name, last_name, email, password, gender, phone, city, address, picture, enable, remember_token, trash, created_at, updated_at):
        self.manage_id = manage_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.gender = gender
        self.phone = phone
        self.city = city
        self.address = address
        self.picture = picture
        self.enable = enable
        self.remember_token = remember_token
        self.trash = trash
        self.created_at = created_at
        self.updated_at = updated_at