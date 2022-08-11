from MySQL_Functions import connect_mysql
from ps_db import pwsin_dict


import datetime
from werkzeug.security import generate_password_hash, check_password_hash



def fetch_time():
	date= datetime.datetime.now()
	date = date.strftime("%Y"+"-"+"%m"+"-"+"%d")
	return date

def fetch_user_name_password(user_name):
	mydb = connect_mysql()
	mycursor = mydb.cursor()
	user_name = (user_name,)
	sql = "SELECT password from crm_employee where email = %s; "
	mycursor.execute (sql, user_name)
	results = mycursor.fetchall()

	return results [0][0]

def secure_password (password):
	return pw_hash

def check_password(pw_hash, password):
	return check_password_hash(pw_hash, password)
 

