from flask import Flask,render_template, url_for ,flash,redirect,session,request,jsonify,json,make_response

app = Flask(__name__)
app.secret_key = '5df4hg5fg4jh56fg4j564gj564hg56j4g5h64j56hg4j5h45j45h4j'

@app.route('/route', methods=('GET','POST'))
def unprotected():
    return jsonify({'message':'show enable'})

if __name__ == '__main__':
    app.run(port=5000,debug=True)