import datetime
from werkzeug.security import generate_password_hash, check_password_hash

def fetch_time():
	date= datetime.datetime.now()
	date = date.strftime("%Y"+"-"+"%m"+"-"+"%d")
	return date

def secure_password (password):
	pw_hash = generate_password_hash(password)
	return pw_hash

def check_password(  pw_hash, password):
	return check_password_hash(pw_hash, password)
 

