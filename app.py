from flask import Flask,redirect,session,request,jsonify,json,make_response
from flask_bcrypt import Bcrypt
from flask_cors import CORS

import random
import jwt
from functools import wraps
import datetime
from datetime import timedelta

app = Flask(__name__)
app.secret_key = '5df4hg5fg4jh56fg4j564gj564hg56j4g5h64j56hg4j5h45j45h4j'


# Route /login api Page
@app.route('/login', methods=('GET','POST'))
def login_jwt():
    u = Users('parwiz')
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