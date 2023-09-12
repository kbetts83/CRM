from flask import Flask, render_template, url_for, flash, redirect,request,session
from forms import Login_Form,Create_Post
from passwords_db import pwsin

from flask_wtf.csrf import CSRFProtect
from flask_ckeditor import CKEditor 
from werkzeug.security import generate_password_hash, check_password_hash

import MySQL_Functions
import blog_functions

import requests

#set the app up
app = Flask(__name__)

#and CK Editor (rich text editor)
ckeditor = CKEditor(app )

#set up security key
app.config['SECRET_KEY'] = pwsin["secret_key"]
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

#ROUTES

#set up the list of projects and languages
project_list = MySQL_Functions.fetch_projects()
language_list = set()
for project in project_list:
    language_list.add (project['language'])

language_list = list(language_list)
print (language_list)

#set route for home page
@app.route("/", )
def home():
    #gets the topic from the html , gets the blog for that topic, returns the informatiom
    topic = request.args.get( "topic", "Blog") #first one is the topic passed from html, 2nd is default
    posts = MySQL_Functions.fetch_blog_entries(topic) 
    tagline = MySQL_Functions.fetch_tagline(topic)
    youtube = MySQL_Functions.fetch_youtube_link(topic)
    github = MySQL_Functions.fetch_github_link(topic)
    link  = MySQL_Functions.fetch_link(topic)


    return render_template('home.html', posts=posts, projects = project_list, 
                                        topic = topic, tagline = tagline,
                                        youtube = youtube, github = github, link = link,
                                        language_list = language_list)

#set route for admin page - i'll add more stuff to this later
@app.route("/admin")
def admin():

    #get the headings and posts for all the blogs
    headings = MySQL_Functions.fetch_blog_headings()
    posts = MySQL_Functions.fetch_all_blogs()

    #get the check id - this is  pretty janky, maybe fix it
    check_id = posts[0]
    check_id = check_id['id']

    return render_template('admin.html', title = 'Admin', projects = project_list, 
            posts = posts, headings = headings, check_id = check_id)

#set route for about page
@app.route("/about")
def about():

    return render_template('about.html', title = 'About', projects = project_list)

#and for the register print
@app.route("/login", methods = ['GET', "POST"], )
def login():
    #get the form info
    form = Login_Form()

    #if the form is correct - ie - must be an email, and the password is filled out
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        pw_hash = MySQL_Functions.fetch_user_name_password()

        #if it's all good
        if username is not None and blog_functions.check_password( pw_hash, password):
            session['user'] = username
            
            #flash the message and redirect
            flash(f"Welcome {form.username.data} !") 
            return redirect(url_for('admin'))

        #if it's not all good
        else:
            flash(f"Incorrect username or email !")   

    return render_template('login.html', title= "login", form = form, projects = project_list)

@app.route("/logout")
def logout():

    session.pop("user", None)
    flash(f"Logged Out !") 
    return redirect(url_for('home'))

@app.route("/create", methods = ['GET', "POST"], )
def create_blog():

    #if there's no user make them login
    if 'user' not in session:
        return redirect(url_for('login'))

    #if they're logged in, have at it
    if 'user' in session:
        user = session['user']

        posts = []
        form = Create_Post()

        if request.method == "POST":

            #get data from the blog and the actual date
            blog_data = request.form
            date = blog_functions.fetch_time()

            #and set up individual variables for the check boxes - maybe I can fix this
            Recursion = request.form.get('knowledge_recursion')
            Algorithms = request.form.get('knowledge_algorithims')
            Data_Structure = request.form.get('knowledge_datastructures')
            OOP = request.form.get('knowledge_OOP') # new starts here
            Git = request.form.get('knoweldge_generators')
            List_Comprehensions = request.form.get('knoweldge_list_comprehensions')
            Dictionary_Comprehensions = request.form.get('knoweldge_dictionary_comprehensions')
            Decorators = request.form.get('knowledge_decorators')

            Python = request.form.get('tech_python')
            HTML = request.form.get('tech_html')
            MySQL = request.form.get('tech_mysql')
            Kivy = request.form.get('tech_kivy')
            Bootstrap = request.form.get('tech_bootstrap')
            Git = request.form.get('tech_git')

            #and post the blog info to the blog table and tech/knowledge data to their own database
            blog_number = MySQL_Functions.post_blog ('Kyle Betts', blog_data['title'], blog_data['blog'], blog_data['project'], date)
            MySQL_Functions.create_knowledge (blog_number, Recursion, Algorithms, Data_Structure,  OOP, Git, List_Comprehensions, Dictionary_Comprehensions, Decorators)
            MySQL_Functions.create_technologies(blog_number,Python, HTML, MySQL, Kivy, Bootstrap, Git)

            #flash and redirect
            flash(f"Blog Post Submitted !") 
            return redirect(url_for('home'))
            
        return render_template('create_blog.html', 
                                title= "create", 
                                form = form, 
                                projects = project_list,)

@app.route("/edit/<int:id>", methods = ['GET', "POST"], )
def edit_blog(id):

    #if there's no user make them login
    if 'user' not in session:
        return redirect(url_for('login'))

    #if they're logged in, have at it
    if 'user' in session:

        #get the post, user, technology and knowledge entries
        user = session['user']
        post = MySQL_Functions.fetch_single_blog_entry(id)

        knowledge = MySQL_Functions.fetch_knowledge_tech (id, 'knowledge')
        tech = MySQL_Functions.fetch_knowledge_tech (id, 'technologies')

        form = Create_Post()

        #fill in the data from the database
        form.title.data = post["title"]
        form.project.data = post["project"]
        form.blog.data = post["content"]

        form.tech_python.data = tech ['python']
        form.tech_html.data = tech ['html']
        form.tech_mysql.data = tech ['mysql']
        form.tech_kivy.data = tech ['kivy']
        form.tech_bootstrap.data = tech ['bootstrap']
        form.tech_git.data = tech ['git']

        form.knowledge_recursion.data = knowledge ['recursion']
        form.knowledge_algorithims.data = knowledge ['algorithms']
        form.knowledge_datastructures.data = knowledge ['Data Structures']


        if request.method == "POST":

            #update teh blog post
            blog_data = request.form
            MySQL_Functions.update_blog(blog_data['title'], blog_data['blog'], blog_data['project'], id)
            
            #update the tech and knolwedge
            Recursion = request.form.get('knowledge_recursion')
            Algorithms = request.form.get('knowledge_datastructures')
            Data_Structure = request.form.get('knowledge_datastructures')

            Python = request.form.get('tech_python')
            HTML = request.form.get('tech_html')
            MySQL = request.form.get('tech_mysql')
            Kivy = request.form.get('tech_kivy')
            Bootstrap = request.form.get('tech_bootstrap')
            Git = request.form.get('tech_git')

            MySQL_Functions.update_knowledge( Recursion, Algorithms, Algorithms, id)
            MySQL_Functions.update_technologies(Python, HTML, MySQL, Kivy, Bootstrap, Git, id)

            #flash and redirect
            flash(f"Blog Post Edit Successful !") 
            return redirect(url_for('admin'))
            
        return render_template('edit_blog.html', 
                                title= "create", 
                                form = form, 
                                projects = project_list,)

@app.route("/delete/<int:id>", methods = ['GET', "POST"], )
def delete_blog(id):

    #if there's no user make them login
    if 'user' not in session:
        return redirect(url_for('login'))

    #if they're logged in, have at it
    if 'user' in session:

        #delete the blog
        MySQL_Functions.delete_blog(id)

        #and flash the message and redirect
        flash(f"Blog {id} deleted !") 
        return redirect(url_for('admin'))
                                
#this launches the server in debug mode
if __name__ == '__main__':
	app.run(debug=False)


