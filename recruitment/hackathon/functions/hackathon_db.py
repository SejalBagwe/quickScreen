import datetime
import sqlite3
import os
import pandas as pd

"""
db_path = os.path.join('\\'.join(os.getcwd().split('\\')[:-2])+'\\db', "hackathon.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT * FROM candidate_info")
rows = cur.fetchall()
#conn.execute("select * from candidate_info")
#rows = conn.fetchall()
print(rows)
conn.close()
"""


def insert_data(Name, Mobile, Start_time, End_time, Attempts, Language, Score):
    db_path = os.path.join(os.getcwd() + '\\db', "hackathon.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = "INSERT INTO candidate_info (name,mobile,start_time,end_time,score,attempts,language) values(?,?,?,?,?,?,?);"
    param = (Name, Mobile, Start_time, End_time, Score, Attempts, Language)

    cur.execute(query, param)
    conn.commit()
    conn.close()
    return
	
def update_data(Mobile,Start_time, End_time,Attempts,Score):
	db_path = os.path.join(os.getcwd() + '\\db', "hackathon.db")
	conn = sqlite3.connect(db_path)
	cur = conn.cursor()
	
	if Score == 100: 
		n_minutes = round((datetime.datetime.strptime(End_time, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(Start_time, '%Y-%m-%d %H:%M:%S.%f')).seconds / 60)
		print(n_minutes)
		if n_minutes > 5:
			n_minutes -= 5
		else:
			n_minutes = 0
			Score = 100 - (n_minutes * 2) - ((Attempts - 1) * 5)

	query = "UPDATE candidate_info SET end_time = ?, score = ?, attempts = ? WHERE mobile = ?"
	param = (End_time, Score, Attempts, Mobile)
	cur.execute(query, param)
	conn.commit()
	conn.close()
	return

def get_data():
	db_path = os.path.join(os.getcwd() + '\\db', "hackathon.db")
	conn = sqlite3.connect(db_path)
	cur = conn.cursor()
	cur.execute("SELECT * FROM candidate_info")
	rows = cur.fetchall()
	data = pd.DataFrame(rows)
	data.columns = ['Id','Name','Mobile','Start Time','End Time','Score','Attempts','Language']
	data.set_index('Id', inplace = True)
	data.sort_values(by=['Id'], ascending=False,inplace=True)
	data.reset_index(drop=True,inplace=True)
	return data
	
def search_license(Key):
	db_path = os.path.join(os.getcwd() + '\\db', "hackathon.db")
	conn = sqlite3.connect(db_path)
	cur = conn.cursor()
	query = "SELECT * FROM license where key = ?"
	param = (Key,)
	print(param)
	cur.execute(query, param)
	rows = cur.fetchall()
	if len(rows) == 0:
		return "Invalid Key"
	data = pd.DataFrame(rows)
	data.columns = ['Key','Status']
	return data
	
def change_status(Key):
	db_path = os.path.join(os.getcwd() + '\\db', "hackathon.db")
	conn = sqlite3.connect(db_path)
	cur = conn.cursor()
	query = "UPDATE license SET status = 'Y' WHERE key = ?"
	param = (Key,)
	cur.execute(query, param)
	conn.commit()
	conn.close()
	return
	
def add_license(Key):
	db_path = os.path.join(os.getcwd() + '\\db', "hackathon.db")
	conn = sqlite3.connect(db_path)
	cur = conn.cursor()
	cur.execute("SELECT status FROM license where key = ?",(Key,))
	rows = cur.fetchall()
	if len(rows) != 0:
		return "Already Exist"
	
	query = "INSERT INTO license (key,status) values(?,?);"
	param = (Key,'N')
	cur.execute(query, param)
	conn.commit()
	conn.close()
	return "Successfully added"