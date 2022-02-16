from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import InputRequired, ValidationError, Length

class LoginForm(FlaskForm):
	username=StringField(validators=[InputRequired(),Length(min=0,max=20)],render_kw={"placeholder":"Username"})
	password = PasswordField(validators=[InputRequired(),Length(min=0,max=30)],render_kw={"placeholder":"Password"})
	submit=SubmitField('Log In')

class RegisterForm(FlaskForm):
	username=StringField(validators=[InputRequired(),Length(min=5,max=20)],render_kw={"placeholder":"Username"})
	password = PasswordField(validators=[InputRequired(),Length(min=5,max=30)],render_kw={"placeholder":"Password"})
	email=StringField(validators=[InputRequired()],render_kw={"placeholder":"Email"})
	submit=SubmitField('Register') 

	## VALDIATING IF THE SAME USER ALREADY EXSISTS OR NOT
	def valdiate_username(self,username):
		old_user=User.query.filter_by(username=username.data).first()
		if old_user:
			raise ValidationError("User already exists")
