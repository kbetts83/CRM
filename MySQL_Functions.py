import mysql.connector 
from ps_db import pwsin_dict

def connect_mysql():
	mydb =mysql.connector.connect(
		host = pwsin_dict["host"],
		user = pwsin_dict["user"],
		passwd= pwsin_dict["passwd"],
		database = pwsin_dict["database"])

	return mydb