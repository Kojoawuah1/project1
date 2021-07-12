from flask import Flask,request,make_response,render_template,jsonify
import flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS , cross_origin

app=Flask(__name__)
CORS(app,resources={r"/mobile/*":{"origins":"*"}})
app.config['CORS HEADERS']='Content-Type'
app.config['SECRET_KEY']="secret"
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True

db=SQLAlchemy(app)

class User(db.Model):
    __tablename__="users"
    
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True)
    password=db.Column(db.String)
    firstname=db.Column(db.String)
    lastname=db.Column(db.String)
db.init_app(app)


@app.route("/",methods=['GET'])
def LoginScreen():
    return render_template("signin.html")

@app.route("/logup",methods=['GET'])
def Logup():
    return render_template("logup.html")


@app.route('/signin',methods=['POST'])
def signin():
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')

        user= User.query.filter((User.email==email) & (User.password == password)).first()
        if user:
            return render_template('home.html',message=user.firstname)
        else:
            return render_template('signin.html')

@app.route("/signup",methods=['POST'])
def handleSignUp():
    if request.method == 'POST':
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        password=request.form.get('password')
        email=request.form.get('email')

        new_user=User(email=email,password=password,firstname=fname,lastname=lname)
        db.session.add(new_user)
        db.session.commit()
        return render_template('/signin.html')


@app.route("/mobile/sign-up",methods=['GET','POST'])
@cross_origin()
def new():
    if request.method=='POST':
        data=request.get_json(force=True)
        new_user=User(email=data['email'],password=data['password'],firstname=data['firstname'],lastname=data['lastname'])
        db.session.add(new_user)
        db.session.commit()
        data={"registered":True,"email":data['email'],'password':data['password']}
    return jsonify(data),200


@app.route("/mobile/login",methods=['POST'])
@cross_origin()
def user():
    if request.method == 'POST':
        data=request.get_json(force=True)
        user=User.query.filter((User.email==data['email']) & (User.password==data['password'])).first()
        if user:
            data={"user":True,"email":user.email,"password":user.password,"firstname":user.firstname}
            return jsonify(data),200
        else :
            data={"user":False}
            return jsonify(data),201


