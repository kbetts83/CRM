from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, Form
from wtforms.validators import DataRequired, Length, Email, EqualTo


class Login_Form(FlaskForm):
	username = EmailField("Username", validators =[DataRequired(), Length(min=2, max=20) ])
	password = PasswordField('Password', validators=[DataRequired()])
	submit  = SubmitField ("Login")



