from flask import Flask,redirect,session,request,jsonify,json,make_response
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random
import jwt
from functools import wraps
import datetime
from datetime import timedelta

app = Flask(__name__)
app.secret_key = '5df4hg5fg4jh56fg4j564gj564hg56j4g5h64j56hg4j5h45j45h4j'
CORS(app)

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/factory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['BASE_URL'] = 'http://127.0.0.1:5000'  # Running on localhost
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True

bcrypt = Bcrypt()

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
    customer_id = db.Column(db.Integer, primary_key = True)
    payment_id = db.Column(db.Integer)
    point_sale_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
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

# Route /sales api
@app.route('/sales', methods=["POST"])
def customerSales():

    #errors = {"first_name" : "first name exists"}
    errors = None
    #success = {"created" : "Employee add successfully."}
    success = None

    customer_id = request.args.get("customer_id")
    payment_id = request.args.get("payment_id")
    point_sale_id = request.args.get("point_sale_id")
    product_id = request.args.get("product_id")
    quantity = request.args.get("quantity")
    paid = request.args.get("paid")
    payment_date = request.args.get("payment_date")

    if payment_id is None:
        errors = {
            "fields" : "Some fields are empty."
        }

    if errors is None:
        customerSales = CustomerSales(customer_id,payment_id,point_sale_id,product_id,10,1,"2020/05/05","2020/05/05")
        db.session.add(customerSales)
        db.session.commit()
        ret = {
            'success':  'customer Sales add successfully.'
        }
        return jsonify(ret), 200
    return jsonify({'errors' : errors})


# get all customers & protected by access token
@app.route('/all_sales/<customer_id>', methods=('GET','POST'))
def all_sales(customer_id):
    data = []
    for x in CustomerSales.query.filter_by(customer_id=customer_id):
        elemenet = { "customer_id" : x.customer_id,
                     "payment_id" : x.payment_id,
                     "point_sale_id" : x.point_sale_id,
                     "product_id" : x.product_id,
                     "quantity" : x.quantity,
                     "paid" : x.paid,
                     "payment_date" : x.payment_date
                    }
        data.append(elemenet)
    return jsonify({ 'data' : data })

# Route /signup api
@app.route('/signup', methods=["POST"])
def signup_jwt():

    #errors = {"first_name" : "first name exists"}
    errors = None
    #success = {"created" : "Employee add successfully."}
    success = None

    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    email = request.args.get("email")
    password = bcrypt.generate_password_hash(request.args.get("password"))
    gender = request.args.get("gender")
    phone = request.args.get("phone")
    city = request.args.get("city")
    address = request.args.get("address")
    picture = request.args.get("picture")

    if first_name is None:
        errors = {
            "fields" : "Some fields are empty."
        }

    data = None
    
    # check if email allready exists.
    data = Customer.query.filter_by(email=email).first()
    if data is not None:
        if data.email == email:
            return jsonify({'email' : 'email allready exists.'})
    
    # check if phone allready exists.
    data = Customer.query.filter_by(phone=phone).first()
    if data is not None:
        if data.phone == phone:
            return jsonify({'phone' : 'phone allready exists.'})

    if errors is None:
        customer = Customer(first_name,last_name,email,password,"gender", 25,phone,"city",address,picture,"credit_card" ,"credit_card_type" ,"billin_address" ,"billing_city" ,"billing_region" ,"billing_postal_code" , "remember_token", "active_token",1, 1, 0,'created_at','updated_at')
        db.session.add(customer)
        db.session.commit()

        data = Customer.query.filter_by(email=email).first()
        
        user = { "id" : data.customer_id,
                     "first_name" : data.first_name,
                     "last_name" : data.last_name,
                     "email" : data.email,
                     "gender" : data.gender,
                     "phone" : data.phone,
                     "city" : data.city,
                     "address" : data.address,
                     "picture" : data.picture,
                     "online" : data.online,
                     "black_list" : data.black_list,
                     "trash" : data.trash,
                     "created_at" : data.created_at,
                     "updated_at" : data.updated_at
                    }
        token = jwt.encode({'user':user,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=1)},app.secret_key)
        ret = {
            'access_token': token.decode('UTF-8'),
            'user':  user,
            'success':  'Employee add successfully.'
        }
        return jsonify(ret), 200
    return jsonify({'errors' : errors})

# Route /signin api
@app.route('/signin', methods=('GET','POST'))
def login_jwt():

    email = request.args.get("email")
    password = request.args.get("password")

    data = Customer.query.filter_by(email=email,password=password).first()

    if data is not None :
        user = { "id" : data.customer_id,
                     "first_name" : data.first_name,
                     "last_name" : data.last_name,
                     "email" : data.email,
                     "gender" : data.gender,
                     "phone" : data.phone,
                     "city" : data.city,
                     "address" : data.address,
                     "picture" : data.picture,
                     "online" : data.online,
                     "black_list" : data.black_list,
                     "trash" : data.trash,
                     "created_at" : data.created_at,
                     "updated_at" : data.updated_at
                    }

        token = jwt.encode({'user':user,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=1)},app.secret_key)
        ret = {
            'token': token.decode('UTF-8'),
            'user':  user
        }
        return jsonify(ret), 200
    return jsonify({'message' : 'Unauthorize.'})

# access_token_required
def access_token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None

        if 'access_token' in request.headers:
            token = request.headers['access_token']

        if not token:
            return jsonify({'message':'token is missing'}), 401

        try:
            data = jwt.decode(token,app.secret_key)
        except :
            return jsonify({'message':'token is invalid'}), 401

        return f(data,*args,**kwargs)

    return decorated

@app.route('/unprotected', methods=('GET','POST'))
def unprotected():
    return jsonify({'message':'show enable'})

@app.route('/protected', methods=('GET','POST'))
@access_token_required
def protected(user):
    print(user)
    return jsonify({'message':user})

# get all customers & protected by access token
@app.route('/all_customers', methods=('GET','POST'))
@access_token_required
def all(user):
    print(user)
    data = []
    for x in Customer.query.all():
        elemenet = { "id" : x.customer_id,
                     "first_name" : x.first_name,
                     "last_name" : x.last_name,
                     "email" : x.email,
                     "gender" : x.gender,
                     "phone" : x.phone,
                     "city" : x.city,
                     "address" : x.address,
                     "picture" : x.picture,
                     "online" : x.online,
                     "black_list" : x.black_list,
                     "trash" : x.trash,
                     "created_at" : x.created_at,
                     "updated_at" : x.updated_at
                    }
        data.append(elemenet)
    return jsonify({ 'data' : data })

# delete employee by id & protected by access token
@app.route('/employee/<id>', methods=['POST'])
def delete(id):
    Customer.query.filter_by(customer_id=6).delete()
    return jsonify({ 'message' : 'delete customer successfully !' })

if __name__ == '__main__':
    app.run(port=5001,debug=True)