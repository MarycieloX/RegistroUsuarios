#from crypt import methods
from email.policy import default
from flask import Flask, render_template, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)


#add datebase
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://admin:123456789@tarea-instance-1.cwntvuamkmig.us-east-1.rds.amazonaws.com/DB_users'
app.config['SQLALCHEMY_TRACK_MODEFICATIONS']=False

# secret key
app.config['SECRET_KEY']='My super secret that no one is supposed to know'

#initialize the database
db=SQLAlchemy(app)

class Users(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(120), nullable=False, unique=True)
    date_added=db.Column(db.DateTime, default= datetime.utcnow)
    
    #create a String
    def __repr__(self):
        return '<Name %r>'% self.name

with app.app_context():
    db.create_all()

#Create form clas
class UserForm(FlaskForm):
    name=StringField("Name", validators=[DataRequired()])
    email=StringField("Email", validators=[DataRequired()])
    submit=SubmitField('Submit')


#create form
class NamerForm(FlaskForm):
    name=StringField("What's your name", validators=[DataRequired()])
    submit=SubmitField('Submit')

@app.route('/')
def index():
    first_name = 'Yo veo doramas'
    stuff='this is bold text'
    flash("welcome to our website")
    favorite_pizza=['Peperony','Calzonee','Hawaiana', 41]

    return render_template('index.html',
    first_name=first_name,
    stuff=stuff,
    favorite_pizza=favorite_pizza)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',
    user_name=name)

@app.route('/name',methods=['GET','POST'])
def name():
    name=None
    form=NamerForm()
    #validate form
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
        flash("From Submitted Successfully")
    return render_template('name.html',
    name=name,
    form=form)


# Add user
@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name=None
    form=UserForm()
    #validate form
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user=Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name=form.name.data
        form.name.data=''
        form.email.data=''
        flash("From Submitted Successfully")
    our_users=Users.query.order_by(Users.date_added)
    return render_template('add_user.html',
    form=form,
    name=name,
    our_users=our_users)

#Delete User
@app.route('/user/delete/<id>')
def delete_user(id):  
    user=Users.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/user/add')

#Upadate User
@app.route('/user/update/<id>',methods=['GET','POST'])
def update_user(id):
    user=Users.query.get(id)
    form=UserForm()
    if form.validate_on_submit():
        user.name=form.name.data
        user.email=form.email.data

        db.session.commit()

    name=form.name.data
    form.name.data=''
    form.email.data=''
    flash("From Submitted Successfully")
    our_users=Users.query.order_by(Users.date_added)

    return render_template('updateUser.html',user=user,form=form,name=name,our_users=our_users)

if __name__ == '__main__':
    app.run(debug=True,port=5000,host="0.0.0.0")
