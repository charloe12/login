
import os
from re import U
from flask import Flask,session,render_template,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='fdojfdoj2'
db = SQLAlchemy(app)
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship( 'User', backref='role', lazy=True)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(64), unique=True, index=True)
    password=db.Column(db.String(64),nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey( 'roles.id'),default=3)
    def __repr__(self):
        return f"{self.username}  {self.role_id}"

class RegistrationForm(FlaskForm):
    username= StringField('username', validators=[DataRequired(), Length(min=2,max=20)])
    password=PasswordField('Password', validators=[DataRequired()])
    submit=SubmitField('Sign Up')

@app.route('/')
def home():
    if 'user' in session:
        res=User.query.all()
        return render_template('index.html',user=res)
    else:
        return redirect(url_for('login'))

@app.route('/register',methods=['post','get'])
def register():
    myform=RegistrationForm()
    if myform.validate_on_submit():
        U=User(username=myform.username.data,password=myform.password.data)
        res=User.query.filter_by(username=myform.username.data).first()
        if res:
            flash('already used')
            return render_template('register.html',form=myform)    

        db.session.add(U)
        db.session.commit()
        return redirect(url_for('login'))   
    return render_template('register.html',form=myform)    


@app.route('/login',methods=['post','get'])
def login():
    myform=RegistrationForm()
    if myform.validate_on_submit():
        res=User.query.filter_by(username=myform.username.data).first()
        if res == None:
            return redirect(url_for('login'))
        else:
            session['user']=res.username
            return redirect(url_for('home'))
    return render_template('login.html',form=myform)


@app.route('/del/<user>')
def dell(user):
    User.query.filter_by(username=user).delete()
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('home'))

if __name__=='__main__':
    app.run(debug=True)