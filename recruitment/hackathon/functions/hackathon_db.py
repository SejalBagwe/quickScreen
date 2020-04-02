import datetime
import sqlite3
import os

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


def insert_data(Name, Mobile, Start_time, End_time, Attempts, Language):
    db_path = os.path.join(os.getcwd() + '\\db', "hackathon.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    n_minutes = round((datetime.datetime.strptime(End_time, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(
        Start_time, '%Y-%m-%d %H:%M:%S.%f')).seconds / 60)
    print(n_minutes)
    if n_minutes > 5:
        n_minutes -= 5
    else:
        n_minutes = 0

    Score = 100 - (n_minutes * 2) - ((Attempts - 1) * 5)

    query = "INSERT INTO candidate_info (name,mobile,start_time,end_time,score,attempts,language) values(?,?,?,?,?,?,?);"
    param = (Name, Mobile, Start_time, End_time, Score, Attempts, Language)

    cur.execute(query, param)
    conn.commit()
    conn.close()
    return
