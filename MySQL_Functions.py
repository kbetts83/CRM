import mysql.connector 
from passwords_db import pwsin

mydb =mysql.connector.connect(
	host = pwsin["host"],
	user = pwsin["user"],
	passwd= pwsin["passwd"],
	database = pwsin["database"])

def fetch_knowledge():
	#function to get the list different types of knowledge
	mycursor = mydb.cursor()
	mycursor.execute ("describe knowledge ")	
	results = mycursor.fetchall()
	knowledge = []
	for result in results:
		knowledge.append(result[0])
	return knowledge
	
def fetch_projects():
	#function to get my list of projects
	mycursor = mydb.cursor()
	mycursor.execute ("SELECT project_name,category from projects; ")
	results = mycursor.fetchall()
	projects = []
	for result in results:
		result_dict =  {"language" : result[1], "project" : result[0]} 
		projects.append(result_dict)

	return tuple (projects)

def fetch_technologies():
	mycursor = mydb.cursor()
	mycursor.execute ("SELECT column_name FROM information_schema.columns WHERE table_name='technologies'; ")
	technologies = mycursor.fetchall()
	return technologies

def fetch_blog_headings():
	#function to get the list different types of knowledge
	mycursor = mydb.cursor()
	mycursor.execute ("describe blog ")	
	results = mycursor.fetchall()
	knowledge = []
	for result in results:
		knowledge.append(result[0])
	return knowledge

def fetch_blog_entries(topic):

	mycursor = mydb.cursor(dictionary=True, )
	sql = """SELECT * FROM blog  
			INNER JOIN knowledge 
			ON blog.id = knowledge.blog_number
			inner join technologies
			on blog.id = technologies.blog_number
			WHERE project = %s """

	var = (topic, )
	mycursor.execute(sql, var )
	blog_entries = mycursor.fetchall()

	return blog_entries


def fetch_all_blogs():
	mycursor = mydb.cursor(dictionary=True, )
	sql = "Select * from blog"
	mycursor.execute(sql,  )
	blog_entries = mycursor.fetchall()
	if blog_entries:
		return blog_entries

	else:
		return [{'id': 0, 'user' : "A girl does not exist", 'content': "No Blog Entries", 'project' : 'none'}]


def fetch_single_blog_entry (id):
	mycursor = mydb.cursor (dictionary = True)
	sql = "select * from blog where id = %s"
	var = (id, )
	mycursor.execute (sql, var)
	blog = mycursor.fetchall()

	return blog[0]

def return_blog_id(results):
	dictionary = (fetch_blog_entries('webscraping')[0])
	return (dictionary["id"])

def post_blog(user,title,content,project, date):
	#enter the blog information
	mycursor = mydb.cursor()
	query = ("INSERT INTO blog"
		"(user,title, content, project, date)"
		"VALUES (%s, %s, %s, %s, %s)")
	values =(user, title ,content, project, date)
	mycursor.execute(query,values)
	mydb.commit()

	#and return the id number
	status_cursor = mydb.cursor()
	status_cursor.execute(f"SELECT LAST_INSERT_ID()")
	results = status_cursor.fetchall()
	return results[0][0]

def update_blog(title,content,project, blog_id):
	#enter the blog information
	mycursor = mydb.cursor()
	sql = """UPDATE blog 
	SET 
    	title = (%s),
    	content =  (%s),
    	project =  (%s)
	WHERE
    id = (%s);
	"""
	values =( title ,content, project, blog_id )
	mycursor.execute(sql,values)
	mydb.commit()


def create_knowledge(blog_number, Recursion, Algorithms, Data_Structures,OOP,Generators,List_Comprehensions,Dictionary_Comprehensions, Decorators):
	mycursor = mydb.cursor()
	query = ("INSERT INTO knowledge"
	"(blog_number, Recursion, Algorithms, `Data Structures`, OOP, Generators, `List Comprehensions`, `Dictionary Comprehensions`, Decorators)"
	"VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)")

	values =(blog_number,Recursion, Algorithms, Data_Structures, OOP,Generators,List_Comprehensions,Dictionary_Comprehensions, Decorators)
	mycursor.execute(query,values)
	mydb.commit()

def update_knowledge( Recursion, Algorithms, Data_Structures, blog_number):
	mycursor = mydb.cursor()
	sql = """UPDATE knowledge 
	SET recursion = %s,
	algorithms = %s,
	`Data Structures` = %s
	WHERE blog_number = %s"""
	val = (Recursion,Algorithms,Data_Structures, blog_number)
	mycursor.execute(sql,val)

	mydb.commit()

def create_technologies(blog_number, Python, HTML, MySQL, Kivy, Bootstrap,Git,):
	mycursor = mydb.cursor()
	query = ("INSERT INTO technologies"
	"(blog_number,Python ,HTML, MySQL, Kivy, Bootstrap, Git)"
	"VALUES (%s,%s, %s, %s, %s, %s, %s)")

	values =(blog_number, Python, HTML, MySQL, Kivy, Bootstrap, Git)
	mycursor.execute(query,values)
	mydb.commit()

def update_technologies(Python, HTML, MySQL, Kivy, Bootstrap, Git, blog_number):
	mycursor = mydb.cursor()

	sql = """UPDATE technologies 
	SET	python = %s , 
		html = %s ,
		MySQL = %s ,
		kivy = %s ,
		bootstrap = %s,
		git = %s
	WHERE blog_number = %s;"""
	val = (Python, HTML, MySQL, Kivy, Bootstrap, Git,  blog_number)
	mycursor.execute(sql,val)
	mydb.commit()

def fetch_user_name_password():
	#function to get the password
	mycursor = mydb.cursor()
	mycursor.execute ("SELECT password from users where email = 'betts.kyle@gmail.com'; ")
	results = mycursor.fetchall()
	return results[0][0]

def fetch_tagline(project):
	#function to get all the tagline for each project
	mycursor = mydb.cursor()
	sql = "SELECT project_description FROM projects WHERE project_name = %s"
	var = (project, )

	mycursor.execute(sql, var)
	tagline= mycursor.fetchall()

	if not tagline:
		return ""
	return tagline[0][0]

def fetch_knowledge_tech(blog_number, category):
	mycursor = mydb.cursor(dictionary = True)
	# get either each technology or knowledge for each blog post
	sql = "SELECT * FROM %s WHERE blog_number = %d" % (category ,blog_number)
	mycursor.execute(sql)
	results = mycursor.fetchall()

	if results:
		return results[0]
	else:
		return {}

def delete_blog(blog_number):
	# #delete the blogs first
	mycursor = mydb.cursor()
	sql = "delete from blog where id = %d" % (blog_number)
	mycursor.execute(sql)
	mydb.commit()

	# #then delete from the knowledge
	mycursor = mydb.cursor()
	sql = "delete from knowledge where blog_number = %d" % (blog_number)
	mycursor.execute(sql)
	mydb.commit()

	# #and delete from technology
	mycursor = mydb.cursor()
	sql = "delete from technologies where blog_number = %d" % (blog_number)
	mycursor.execute(sql)
	mydb.commit()

def fetch_youtube_link(project):
	mycursor = mydb.cursor()
	sql = "select youtube from projects where project_name = '%s'" % (project)
	mycursor.execute(sql)
	results = mycursor.fetchall()
	if results:
		return results[0][0]
	else:
		return None

def fetch_github_link(project):
	mycursor = mydb.cursor()
	sql = "select github from projects where project_name = '%s'" % (project)
	mycursor.execute(sql)
	results = mycursor.fetchall()
	if results:
		return results[0][0]
	else:
		return None

def fetch_link(project):
	mycursor = mydb.cursor()
	sql = "select link from projects where project_name = '%s'" % (project)
	mycursor.execute(sql)
	results = mycursor.fetchall()
	if results:
		return results[0][0]
	else:
		return None

