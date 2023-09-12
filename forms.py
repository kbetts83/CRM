from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, Form, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_ckeditor import CKEditorField

from MySQL_Functions import fetch_technologies,fetch_knowledge, fetch_projects

class Login_Form(FlaskForm):
	username = StringField("Username", validators =[DataRequired(), Length(min=2, max=20) ])
	password = PasswordField('Password', validators=[DataRequired()])
	submit  = SubmitField ("Login")

class Create_Post(FlaskForm):
	#create list for projects
	title = StringField("Title", validators =[DataRequired()])
	project = SelectField("Project", choices = (fetch_projects() ) ) #<-- weird glitch started happening, fix it
	blog = CKEditorField("Blog", validators =[DataRequired(), Length(min=1, max=2000) ])
	submit  = SubmitField ("Post")

	#now checkboxes for the technology 	update this to dynamically load
	tech_python = BooleanField("Python",)
	tech_mysql = BooleanField("MySQL",)
	tech_kivy = BooleanField("Kivy",)
	tech_html = BooleanField ("HTML",)
	tech_bootstrap = BooleanField("Bootstrap",)
	tech_git = BooleanField("Git",)

	#and knowledge
	knowledge_recursion = BooleanField("Recursion",  )
	knowledge_algorithims = BooleanField("Algorithms",  )
	knowledge_datastructures = BooleanField("`Data Structures`", )
	
	knowledge_OOP = BooleanField("OOP",) # add here - databse done
	knoweldge_generators = BooleanField("Generators",) # add here databse done
	knoweldge_list_comprehensions = BooleanField("`List Comprehensions`")# add here database done
	knoweldge_dictionary_comprehensions = BooleanField("`Dictionary Comprehensions`",)# add here database done
	knowledge_decorators = BooleanField ("Decorators",)# add here database done

