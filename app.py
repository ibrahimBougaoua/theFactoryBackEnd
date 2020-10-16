from flask import Flask,redirect,session,request,jsonify,json,make_response
from models.__init__ import app,db  
from models.customer import Customer
from models.payment import Payment
from models.pointOfSale import PointOfSale
from models.category import Category
from models.product import Product
from models.customerSales import CustomerSales
from models.factory import Factory
from models.picture import Picture
from models.employeePointOfSale import EmployeePointOfSale
from models.store import Store
from flask_cors import CORS
import random
import jwt
from functools import wraps
import datetime
from datetime import timedelta

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BASE_URL'] = 'http://127.0.0.1:5000'  # Running on localhost
app.config['JWT_SECRET_KEY'] = 'f98*-+/h-fg/j-8gf-8j-g*8j*g8j*8*fgh*re8h*re8*8f8h-*f8'  # Change this!
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True

CORS(app)

if __name__ == '__main__':
    app.run(port=5000,debug=True)