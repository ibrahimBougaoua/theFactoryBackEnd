from flask import Flask,redirect,session,request,jsonify,json,make_response
from models.__init__ import app,db  
from models.customer import Customer
from models.payment import Payment
from models.pointOfSale import PointOfSale
from models.category import Category
from models.product import Product
from models.customerSales import CustomerSales
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import random
import jwt
from functools import wraps
import datetime
from datetime import timedelta

CORS(app)
bcrypt = Bcrypt()

# Route /sales api
@app.route('/new/sale', methods=["POST"])
def customerSales():

    #errors = {"first_name" : "first name exists"}
    errors = {}
    #success = {"created" : "Employee add successfully."}
    success = None

    if request.method == 'POST':

        customer_id = request.args.get("customer_id")
        if not customer_id:
            errors["customer_id"] = "customer_id is empty."

        payment_id = request.args.get("payment_id")
        if not payment_id:
            errors["payment_id"] = "payment_id is empty."

        point_sale_id = request.args.get("point_sale_id")
        if not point_sale_id:
            errors["point_sale_id"] = "point_sale_id is empty."

        product_id = request.args.get("product_id")
        if not product_id:
            errors["product_id"] = "product_id is empty."

        quantity = request.args.get("quantity")
        if not quantity:
            errors["quantity"] = "quantity is empty."

        paid = request.args.get("paid")
        if not paid:
            paid = 1

        payment_date = request.args.get("payment_date")

        if payment_id is None:
            errors = {
                "fields" : "Some fields are empty."
            }

        if errors:
            return jsonify({'data' : { 'errors' : errors } })
        else:
            customerSales = CustomerSales(customer_id,payment_id,point_sale_id,product_id,quantity,int(paid),payment_date,"2020/05/05")
            db.session.add(customerSales)
            db.session.commit()
            ret = {
                'success':  'customer Sales add successfully.'
            }
            return jsonify(ret), 200
        return jsonify({'errors' : errors})

    return jsonify({'errors' : 'the request not allow !'})



# update sale by id & protected by access token
@app.route('/sale/update/<id>', methods=['PUT'])
def updateCustomerSaleById(id):

    errors = {}

    customerSales = customerSales.query.get(id)

    if customerSales is not None:
        if request.method == 'PUT':

            quantity = request.args.get("quantity")
            if quantity:
                if len(quantity) > 0:
                    customerSales.quantity = quantity
                else:
                    errors["quantity"] = "quantity most be > 0."
            else:
                errors["quantity"] = "quantity is empty."

            paid = request.args.get("paid")
            if paid:
                customerSales.paid = paid

            payment_date = request.args.get("payment_date")
            if payment_date:
                customerSales.payment_date = payment_date

            if errors:
                return jsonify({'data' : { 'errors' : errors } })
            else:
                db.session.commit()
                return jsonify({'data' : {  'success' : 'customer sale update successfully.' } })

    else:
        errors["sale"] = "sale not found."
    
    return jsonify({'data' : {  'errors' : errors } })

# get all customers & protected by access token
@app.route('/all_sales/<customer_id>', methods=('GET','POST'))
def all_sales(customer_id):
    data = []
    print(CustomerSales.query.all())
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
def allCustomers(user):
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
    return jsonify({'data' : {  'customers' : data } })

# update customer by id & protected by access token
@app.route('/customer/update/<id>', methods=['PUT'])
def updateCustomerById(id):

    errors = {}

    customer = Customer.query.get(id)

    if customer is not None:
        if request.method == 'PUT':

            first_name = request.args.get("first_name")
            if first_name:
                if len(first_name) > 4:
                    customer.first_name = first_name
                else:
                    errors["first_name"] = "first name most be > 4 caracter."
            else:
                errors["first_name"] = "first name is empty."

            last_name = request.args.get("last_name")
            if last_name:
                if len(last_name) > 4:
                    customer.last_name = last_name
                else:
                    errors["last_name"] = "last name most be > 4 caracter."
            else:
                errors["last_name"] = "last name is empty."

            email = request.args.get("email")
            if email:
                customer.email = email
            else:
                errors["email"] = "email is empty."

            password = request.args.get("password")
            if password:
                if len(password) > 7:
                    customer.password = password
                else:
                    errors["password"] = "password most be >= 8 caracter."

            gender = request.args.get("gender")
            if gender:
                customer.gender = gender
            else:
                errors["gender"] = "gender is empty."

            age = request.args.get("age")
            if age:
                customer.age = age
            else:
                errors["age"] = "age is empty."

            phone = request.args.get("phone")
            if phone:
                if len(phone) == 10:
                    customer.phone = phone
                else:
                    errors["phone"] = "phone most be 10 caracter."
            else:
                errors["phone"] = "phone is empty."

            city = request.args.get("city")
            if city:
                customer.city = city
            else:
                errors["city"] = "city is empty."

            address = request.args.get("address")
            if address:
                if len(address) > 5:
                    customer.address = address
                else:
                    errors["address"] = "address most be > 5 caracter."
            else:
                errors["address"] = "address is empty."

            picture = request.args.get("picture")
            if picture:
                customer.picture = picture
            else:
                errors["picture"] = "picture is empty."

            credit_card = request.args.get("credit_card")
            if credit_card:
                customer.credit_card = credit_card
            else:
                errors["credit_card"] = "credit card is empty."

            credit_card_type = request.args.get("credit_card_type")
            if credit_card_type:
                customer.credit_card_type = credit_card_type
            else:
                errors["credit_card_type"] = "credit card type is empty."

            billin_address = request.args.get("billin_address")
            if billin_address:
                customer.billin_address = billin_address
            else:
                errors["billin_address"] = "billin address is empty."

            billing_city = request.args.get("billing_city")
            if billing_city:
                customer.billing_city = billing_city
            else:
                errors["billing_city"] = "billing city is empty."

            billing_region = request.args.get("billing_region")
            if billing_region:
                customer.billing_region = billing_region
            else:
                errors["billing_region"] = "billing region is empty."

            billing_postal_code = request.args.get("billing_postal_code")
            if billing_postal_code:
                customer.billing_postal_code = billing_postal_code
            else:
                errors["billing_postal_code"] = "billing postal code is empty."

            if errors:
                return jsonify({'data' : { 'errors' : errors } })
            else:
                db.session.commit()
                return jsonify({'data' : {  'success' : 'customer update successfully.' } })

    else:
        errors["customer"] = "customer not found."
    
    return jsonify({'data' : {  'errors' : errors } })

# delete customer by id & protected by access token
@app.route('/customer/delete/<id>', methods=['DELETE'])
def deleteCustomerById(id): 
    if request.method == 'DELETE':
        customer = Customer.query.get(id)
        if customer is not None:
            Customer.query.filter_by(customer_id=id).delete()
            db.session.commit()
            return jsonify({'data' : {  'success' : 'delete customer successfully.' } })
        return jsonify({'data' : {  'errors' : 'customer not found.' } })

# delete customer by id & protected by access token
@app.route('/sales/delete/<id>', methods=['DELETE'])
def deleteCustomerSalesById(id): 
    if request.method == 'DELETE':
        customerSales = CustomerSales.query.get(id)
        if customerSales is not None:
            CustomerSales.query.filter_by(customer_id=id).delete()
            db.session.commit()
            return jsonify({'data' : {  'success' : 'delete customer sales successfully.' } })
        return jsonify({'data' : {  'errors' : 'customer sales not found.' } })

if __name__ == '__main__':
    app.run(port=5001,debug=True)