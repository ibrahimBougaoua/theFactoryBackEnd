from flask import Flask,redirect,session,request,jsonify,json,make_response
from models.__init__ import app,db  
from models.employee import Employee
from models.pointOfSale import PointOfSale
from models.category import Category
from models.picture import Picture
from models.product import Product
from models.store import Store
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import random
import jwt
from functools import wraps
import datetime
from datetime import timedelta

app.config['BASE_URL'] = 'http://127.0.0.1:5002'  # Running on localhost
app.config['JWT_SECRET_KEY'] = 'f98*-+/h-fg/j-8gf-8j-g*8j*g8j*8*fgh*re8h*re8*8f8h-*f8'  # Change this!
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True

CORS(app)
bcrypt = Bcrypt()

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
    manage_id = request.args.get("manage_id")

    if first_name is None:
        errors = {
            "fields" : "Some fields are empty."
        }

    data = None
    
    # check if email allready exists.
    data = Employee.query.filter_by(email=email).first()
    if data is not None:
        if data.email == email:
            return jsonify({'email' : 'email allready exists.'})
    
    # check if phone allready exists.
    data = Employee.query.filter_by(phone=phone).first()
    if data is not None:
        if data.phone == phone:
            return jsonify({'phone' : 'phone allready exists.'})

    # check if the manager is exist.
    data = Employee.query.filter_by(employee_id=manage_id).first()
    if data is None:
            return jsonify({'manager' : 'not exist.'})

    if errors is None:

        employee = Employee(manage_id,first_name,last_name,email,password,"gender",phone,"city",address,picture,0,'remember_token',0,'created_at','updated_at')
        db.session.add(employee)
        db.session.commit()

        data = Employee.query.filter_by(email=email).first()
        
        user = { "id" : data.employee_id,
                     "first_name" : data.first_name,
                     "last_name" : data.last_name,
                     "email" : data.email,
                     "gender" : data.gender,
                     "phone" : data.phone,
                     "city" : data.city,
                     "address" : data.address,
                     "picture" : data.picture,
                     "enable" : data.enable,
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

    data = Employee.query.filter_by(email=email,password=password).first()

    if data is not None :
        user = { "id" : data.employee_id,
                     "first_name" : data.first_name,
                     "last_name" : data.last_name,
                     "email" : data.email,
                     "gender" : data.gender,
                     "phone" : data.phone,
                     "city" : data.city,
                     "address" : data.address,
                     "picture" : data.picture,
                     "enable" : data.enable,
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

# get all emploies & protected by access token
@app.route('/all_employee', methods=('GET','POST'))
@access_token_required
def all(user):
    print(user)
    data = []
    for x in Employee.query.all():
        elemenet = { "id" : x.employee_id,
                     "first_name" : x.first_name,
                     "last_name" : x.last_name,
                     "email" : x.email,
                     "gender" : x.gender,
                     "phone" : x.phone,
                     "city" : x.city,
                     "address" : x.address,
                     "picture" : x.picture,
                     "enable" : x.enable,
                     "trash" : x.trash,
                     "created_at" : x.created_at,
                     "updated_at" : x.updated_at
                    }
        data.append(elemenet)
    return jsonify({ 'data' : data })

# delete employee by id & protected by access token
@app.route('/employee/<id>', methods=['POST'])
def delete(id):
    Employee.query.filter_by(employee_id=6).delete()
    return jsonify({ 'message' : 'delete employee successfully !' })



# Route /new/store api
@app.route('/new/store', methods=["POST"])
def CreateStore():

    #errors = {"first_name" : "first name exists"}
    errors = {}
    #success = {"created" : "Employee add successfully."}
    success = None

    if request.method == 'POST':

        point_sale_id = request.args.get("point_sale_id")
        if not point_sale_id:
            errors["point_sale_id"] = "point_sale_id is empty."

        product_id = request.args.get("product_id")
        if not product_id:
            errors["product_id"] = "product_id is empty."

        quantity_store = request.args.get("quantity_store")
        if not quantity_store:
            errors["quantity_store"] = "quantity_store is empty."

        quantity_sold = request.args.get("quantity_sold")
        if not quantity_sold:
            errors["quantity_sold"] = "quantity_sold is empty."

        if point_sale_id is None:
            errors = {
                "fields" : "Some fields are empty."
            }

        if errors:
            return jsonify({'data' : { 'errors' : errors } })
        else:
            store = Store(point_sale_id,product_id,quantity_store,quantity_sold)
            db.session.add(store)
            db.session.commit()
            ret = {
                'success':  'store added successfully.'
            }
            return jsonify(ret), 200
        return jsonify({'errors' : errors})

    return jsonify({'errors' : 'the request not allow !'})

# update store by id & protected by access token
@app.route('/store/update/<id>', methods=['PUT'])
def updateStoreById(id):

    errors = {}

    store = Store.query.get(id)

    if store is not None:
        if request.method == 'PUT':

            point_sale_id = request.args.get("point_sale_id")
            if point_sale_id:
                store.point_sale_id = point_sale_id

            product_id = request.args.get("product_id")
            if product_id:
                store.product_id = product_id

            quantity_store = request.args.get("quantity_store")
            if quantity_store:
                if int(quantity_store) > 0:
                    store.quantity_store = quantity_store
                else:
                    errors["quantity_store"] = "quantity_store most be > 0."
            else:
                errors["quantity_store"] = "quantity_store is empty."

            quantity_sold = request.args.get("quantity_sold")
            if quantity_sold:
                if int(quantity_sold) > 0:
                    store.quantity_sold = quantity_sold
                else:
                    errors["quantity_sold"] = "quantity_sold most be > 0."
            else:
                errors["quantity_sold"] = "quantity_sold is empty."


            if errors:
                return jsonify({'data' : { 'errors' : errors } })
            else:
                db.session.commit()
                return jsonify({'data' : {  'success' : 'store update successfully.' } })

    else:
        errors["store"] = "store not found."
    
    return jsonify({'data' : {  'errors' : errors } })


# delete store by id & protected by access token
@app.route('/store/delete/<id>', methods=['DELETE'])
def deleteStoreById(id): 
    if request.method == 'DELETE':
        store = Store.query.get(id)
        if store is not None:
            Store.query.filter_by(id=id).delete()
            db.session.commit()
            return jsonify({'data' : {  'success' : 'delete store successfully.' } })
        return jsonify({'data' : {  'errors' : 'store not found.' } })

# Route /add/product api
@app.route('/add/product', methods=["POST"])
def addProduct():

    #errors = {"first_name" : "first name exists"}
    errors = {}
    #success = {"created" : "Employee add successfully."}
    success = None

    if request.method == 'POST':

        name = request.args.get("name")
        if not name:
            errors["name"] = "name is empty."

        desc = request.args.get("desc")
        if not desc:
            errors["desc"] = "desc is empty."

        quantity_unit = request.args.get("quantity_unit")
        if quantity_unit:
            if int(quantity_unit) < 0:
                errors["quantity_unit"] = "quantity_unit most be > 0."
        else:
            errors["quantity_unit"] = "quantity_unit is empty."

        unit_price = request.args.get("unit_price")
        if unit_price:
            if int(unit_price) < 0:
                errors["unit_price"] = "unit_price most be > 0."
        else:
            errors["unit_price"] = "unit_price is empty."

        size = request.args.get("size")
        if not size:
            errors["size"] = "size is empty."

        color = request.args.get("color")
        if not color:
            errors["color"] = "color is empty."

        note = request.args.get("note")
        if not note:
            errors["note"] = "note is empty."

        category_id = request.args.get("category_id")
        if not category_id:
            errors["category_id"] = "category_id is empty."

        if name is None:
            errors = {
                "fields" : "Some fields are empty."
            }

        if errors:
            return jsonify({'data' : { 'errors' : errors } })
        else:
            product = Product(name, desc, quantity_unit, unit_price, size, color, note,category_id)
            db.session.add(product)
            db.session.commit()
            ret = {
                'success':  'product added successfully.'
            }
            return jsonify(ret), 200
        return jsonify({'errors' : errors})

    return jsonify({'errors' : 'the request not allow !'})

# update product by id & protected by access token
@app.route('/product/update/<id>', methods=['PUT'])
def updateStoreById(id):

    errors = {}

    product = Product.query.get(id)

    if product is not None:
        if request.method == 'PUT':

            name = request.args.get("name")
            if name:
                product.name = name

            desc = request.args.get("desc")
            if desc:
                product.desc = desc

            quantity_unit = request.args.get("quantity_unit")
            if quantity_unit:
                if int(quantity_unit) > 0:
                    product.quantity_unit = quantity_unit
                else:
                    errors["quantity_unit"] = "quantity_unit most be > 0."
            else:
                errors["quantity_unit"] = "quantity_unit is empty."

            quantity_unit = request.args.get("quantity_unit")
            if quantity_unit:
                if int(quantity_unit) > 0:
                    product.quantity_unit = quantity_unit
                else:
                    errors["quantity_unit"] = "quantity_unit most be > 0."
            else:
                errors["quantity_unit"] = "quantity_unit is empty."

            unit_price = request.args.get("unit_price")
            if unit_price:
                if int(unit_price) > 0:
                    store.unit_price = unit_price
                else:
                    errors["unit_price"] = "unit_price most be > 0."
            else:
                errors["unit_price"] = "unit_price is empty."


            size = request.args.get("size")
            if size:
                product.size = size

            color = request.args.get("color")
            if color:
                product.color = color

            note = request.args.get("note")
            if note:
                product.note = note

            if errors:
                return jsonify({'data' : { 'errors' : errors } })
            else:
                db.session.commit()
                return jsonify({'data' : {  'success' : 'product update successfully.' } })

    else:
        errors["product"] = "product not found."
    
    return jsonify({'data' : {  'errors' : errors } })


# delete product by id & protected by access token
@app.route('/product/delete/<id>', methods=['DELETE'])
def deleteProductById(id): 
    if request.method == 'DELETE':
        product = Product.query.get(id)
        if product is not None:
            Product.query.filter_by(id=id).delete()
            db.session.commit()
            return jsonify({'data' : {  'success' : 'delete product successfully.' } })
        return jsonify({'data' : {  'errors' : 'product not found.' } })

# Route /add/category api
@app.route('/add/category', methods=["POST"])
def addCategory():

    #errors = {"first_name" : "first name exists"}
    errors = {}
    #success = {"created" : "Employee add successfully."}
    success = None

    if request.method == 'POST':

        name = request.args.get("name")
        if not name:
            errors["name"] = "name is empty."

        slug = request.args.get("slug")
        if not slug:
            errors["slug"] = "slug is empty."

        description = request.args.get("description")
        if not description:
            errors["description"] = "description is empty."

        if name is None:
            errors = {
                "fields" : "Some fields are empty."
            }

        if errors:
            return jsonify({'data' : { 'errors' : errors } })
        else:
            category = Category(name, slug, description)
            db.session.add(category)
            db.session.commit()
            ret = {
                'success':  'category added successfully.'
            }
            return jsonify(ret), 200
        return jsonify({'errors' : errors})

    return jsonify({'errors' : 'the request not allow !'})

# update category by id & protected by access token
@app.route('/category/update/<id>', methods=['PUT'])
def updateCategoryById(id):

    errors = {}

    category = Category.query.get(id)

    if category is not None:
        if request.method == 'PUT':

            name = request.args.get("name")
            if name:
                category.name = name

            slug = request.args.get("slug")
            if slug:
                category.slug = slug

            description = request.args.get("description")
            if description:
                category.description = description

            if errors:
                return jsonify({'data' : { 'errors' : errors } })
            else:
                db.session.commit()
                return jsonify({'data' : {  'success' : 'category update successfully.' } })

    else:
        errors["category"] = "category not found."
    
    return jsonify({'data' : {  'errors' : errors } })


# delete category by id & protected by access token
@app.route('/category/delete/<id>', methods=['DELETE'])
def deleteCategoryById(id): 
    if request.method == 'DELETE':
        category = Category.query.get(id)
        if category is not None:
            Category.query.filter_by(id=id).delete()
            db.session.commit()
            return jsonify({'data' : {  'success' : 'delete category successfully.' } })
        return jsonify({'data' : {  'errors' : 'category not found.' } })



# Route /add/picture api
@app.route('/add/picture', methods=["POST"])
def addPicture():

    #errors = {"first_name" : "first name exists"}
    errors = {}
    #success = {"created" : "Employee add successfully."}
    success = None

    if request.method == 'POST':

        name = request.args.get("name")
        if not name:
            errors["name"] = "name is empty."

        size = request.args.get("size")
        if not size:
            errors["size"] = "size is empty."

        product_id = request.args.get("product_id")
        if not product_id:
            errors["product_id"] = "product_id is empty."

        if name is None:
            errors = {
                "fields" : "Some fields are empty."
            }

        if errors:
            return jsonify({'data' : { 'errors' : errors } })
        else:
            picture = Picture(name, size, product_id)
            db.session.add(picture)
            db.session.commit()
            ret = {
                'success':  'picture added successfully.'
            }
            return jsonify(ret), 200
        return jsonify({'errors' : errors})

    return jsonify({'errors' : 'the request not allow !'})

# update picture by id & protected by access token
@app.route('/picture/update/<id>', methods=['PUT'])
def updatePictureById(id):

    errors = {}

    picture = Picture.query.get(id)

    if picture is not None:
        if request.method == 'PUT':

            name = request.args.get("name")
            if name:
                picture.name = name

            size = request.args.get("size")
            if size:
                picture.size = size

            product_id = request.args.get("product_id")
            if product_id:
                picture.product_id = product_id

            if errors:
                return jsonify({'data' : { 'errors' : errors } })
            else:
                db.session.commit()
                return jsonify({'data' : {  'success' : 'picture update successfully.' } })

    else:
        errors["picture"] = "picture not found."
    
    return jsonify({'data' : {  'errors' : errors } })


# delete picture by id & protected by access token
@app.route('/picture/delete/<id>', methods=['DELETE'])
def deletePictureById(id): 
    if request.method == 'DELETE':
        picture = Picture.query.get(id)
        if picture is not None:
            Picture.query.filter_by(id=id).delete()
            db.session.commit()
            return jsonify({'data' : {  'success' : 'delete picture successfully.' } })
        return jsonify({'data' : {  'errors' : 'picture not found.' } })

if __name__ == '__main__':
    app.run(port=5002,debug=True)