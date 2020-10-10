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

# Route /login api Page
@app.route('/login', methods=('GET','POST'))
def login_jwt():
    u = Employee(1,'parwiz','parwiz','parwiz','parwiz','parwiz','parwiz','parwiz','parwiz','parwiz',0,'parwiz',0,'parwiz','parwiz')
    db.session.add(u)
    db.session.commit()
    username = "ibrahim"
    password = "bougaoua"
    user = {
        "id":1,
        "a":"b",
        "a":"b"
    }

    if not username or not password:
        return make_response('Could not verify',401,{'WWW-Authenticate':'Basic releam="Login required"'})

    if username is not None:
        token = jwt.encode({'username':"ibrahim",'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.secret_key)
        ret = {
            'token': token.decode('UTF-8'),
            'user':  user
        }
        return jsonify(ret), 200
    return make_response('Could not verify',401,{'WWW-Authenticate':'Basic releam="Login required"'})

# token_required
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

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
@token_required
def protected(user):
    print(user)
    return jsonify({'message':user})

if __name__ == '__main__':
    app.run(port=5000,debug=True)