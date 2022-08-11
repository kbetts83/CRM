from flask import Flask, render_template, url_for, flash, redirect,request,session
from CRM_WTF_Forms import Login_Form

from flask_wtf.csrf import CSRFProtect
from flask_ckeditor import CKEditor 
from werkzeug.security import generate_password_hash, check_password_hash

from ps_db import pwsin_dict
import MySQL_Functions
import CRM_Password_Functions


import requests

#set the app up
app = Flask(__name__)

#set up security key
app.config['SECRET_KEY'] = pwsin_dict ['secret_key']
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

agent_id = 1

#set route for home page
@app.route("/", )
def login_filter():


    #if there's no user make them login
    if 'user' not in session:
        return redirect(url_for('login'))

    #if they're logged in, have at it
    if 'user' in session:
        return redirect(url_for('stats'))

@app.route("/stats")
def stats():

    #get the page name so we can pass it into Jinja
    page = str(request.url_rule)

    return render_template('nav_pages.html', page = page)

@app.route("/work_space")
def work_space():
    #get the page name so we can pass it into Jinja
    page = str(request.url_rule)


    return render_template('nav_pages.html', page = page)

#and for the register print
@app.route("/login", methods = ['GET', "POST"], )
def login():
    #get the form info
    form = Login_Form()

    #if the form is correct - ie - must be an email, and the password is filled out
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        pw_hash = CRM_Password_Functions.fetch_user_name_password(username)

        #if it's all good
        if username is not None and CRM_Password_Functions.check_password( pw_hash, password):
            session['user'] = username
            
            #flash the message and redirect
            flash(f"Welcome {form.username.data} !") 
            return redirect(url_for('stats'))

        #if it's not all good
        else:
            print ("Email or password not correct") 

    return render_template('login.html', form = form, agent_id = agent_id)

@app.route("/logout")
def logout():

    session.pop("user", None)
    flash(f"Logged Out !") 
    return redirect(url_for('login_filter'))
                                
#this launches the server in debug mode
if __name__ == '__main__':
	app.run(debug=False)


