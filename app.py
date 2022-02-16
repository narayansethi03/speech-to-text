from flask import Flask
from flask import render_template,redirect,url_for,request,abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user
from flask_bcrypt import Bcrypt
from form import LoginForm, RegisterForm
import speech_recognition as speech
import os

app=Flask(__name__)
bcrypt=Bcrypt(app)

app.config['SECRET_KEY']='abcd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login' 

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

db=SQLAlchemy(app)
Migrate(app,db)

class User(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String (50),unique=True)
	password = db.Column(db.String(250))

	def __init__(self,username,password,email):
		self.username=username
		self.password=password	
		self.email=email

db.create_all()


	
@app.route('/')
def index():
	return render_template ('index.html')

@app.route('/login',methods=['GET','POST'])
def login(): 
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.username.data).first()
		if user:
			if  bcrypt.check_password_hash(user.password,form.password.data):
				login_user(user)
				#return f"done"
				return redirect (url_for('add_audio',name=form.username.data))
		
		
		flash ("Wrong Credentials!")


	return render_template ('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():

	form=RegisterForm()
	if form.validate_on_submit():

		hashed_password=bcrypt.generate_password_hash(form.password.data)
		new_user=User(username=form.username.data,password=hashed_password,email=form.email.data)
		db.session.add(new_user)
		db.session.commit()

		return redirect (url_for('login'))

	return render_template ('register.html',form=form)

@app.route('/add_audio',methods=['GET','POST'])
@login_required
def add_audio():
	text=""
	if request.method=='POST':

		file=request.files['file']

		if file:
			recogonizer = speech.Recognizer() #function in module to recogonize spech
			audioFile = speech.AudioFile(file) #funcation to take in the audio
			with audioFile as source: #opening audio as 'source' 
				data = recogonizer.record (source) #using pre defined funcation to reading audio
			text = recogonizer.recognize_google (data,key=None) #transcribing		
			return render_template ('text.html',text=text)

	return render_template('add_audio.html')

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash ("You've been succesfully Logged Out!")
	return render_template('index.html')


	


if __name__ =='__main__':
	app.run(debug=True,threaded=True)