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
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "hackathon.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    minutes = 0
    Date = str(datetime.datetime.strptime(Start_time, '%Y-%m-%d %H:%M:%S.%f').date())
    Time = str(datetime.datetime.strptime(Start_time, '%Y-%m-%d %H:%M:%S.%f').time().replace(microsecond=0))
    query = "INSERT INTO candidate_info (name,mobile,start_time,end_time,score,attempts,language,date,time,minutes,Code) values(?,?,?,?,?,?,?,?,?,?,?);"
    param = (Name, Mobile, Start_time, End_time, Score, Attempts, Language,Date,Time,minutes,"NA")

    cur.execute(query, param)
    conn.commit()
    conn.close()
    return

def update_data(Mobile,Start_time, End_time,Attempts,Score,Fail=False):
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "hackathon.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if not Fail:
        minutes = 0
        Code = "NA"
        if Score == 100:
            minutes = round((datetime.datetime.strptime(End_time, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(Start_time, '%Y-%m-%d %H:%M:%S.%f')).seconds / 60)
            print(minutes)
            if minutes > 10:
                n_minutes = minutes - 10
            else:
                n_minutes = 0
            Score = 100 - (n_minutes * 2)
            Code = "PASS"
        print(Score,'\n',Attempts)
        query = "UPDATE candidate_info SET end_time = ?, score = ?, attempts = ?, minutes = ?, code = ? WHERE id = (select MAX(id) from candidate_info where mobile = ?)"
        param = (End_time, int(Score), int(Attempts), int(minutes), Code, Mobile)
        cur.execute(query, param)
    else:
        minutes = 25
        Code = "FAIL"
        query = "UPDATE candidate_info SET minutes = ?, code = ? WHERE id = (select MAX(id) from candidate_info where mobile = ?)"
        param = (int(minutes), Code, Mobile)
        cur.execute(query, param)
    conn.commit()
    conn.close()
    return

def get_data():
    # print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "hackathon.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM candidate_info")
    rows = cur.fetchall()
    data = pd.DataFrame(rows)
    data.columns = ['Id','Name','Mobile','Start Time','End Time','Score','Attempts','Language','Date','Time','Minutes','Code']
    data.set_index('Id', inplace = True)
    data.sort_values(by=['Id'], ascending=False,inplace=True)
    data.reset_index(drop=True,inplace=True)
    return data

def search_license(Key):
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "hackathon.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if Key == 'ALL':
        query = "SELECT * FROM license"
        cur.execute(query)
    else:
        query = "SELECT * FROM license where key = ?"
        param = (Key,)
        cur.execute(query, param)
    rows = cur.fetchall()
    if len(rows) == 0:
        return "An invalid license key."
    data = pd.DataFrame(rows)
    data.columns = ['Key','Status']
    data.sort_values(by=['Status'],ascending=False,inplace=True)
    data.reset_index(drop=True, inplace=True)
    return data

def change_status(Status,Key):
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "hackathon.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT status FROM license where key = ?",(Key,))
    rows = cur.fetchall()
    if len(rows) == 0:
        return "License key does not exists."

    query = "UPDATE license SET status = ? WHERE key = ?"
    param = (Status,Key)
    cur.execute(query, param)
    conn.commit()
    conn.close()
    return 'Status of key change to "New".'

def add_license(Key):
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "hackathon.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT status FROM license where key = ?",(Key,))
    rows = cur.fetchall()
    if len(rows) != 0:
        return "License key already exists."

    query = "INSERT INTO license (key,status) values(?,?);"
    param = (Key,'N')
    cur.execute(query, param)
    conn.commit()
    conn.close()
    return "License key has been successfully added."

def del_license(Key,All=False):
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "hackathon.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if not All:
        cur.execute("SELECT status FROM license where key = ?",(Key,))
        rows = cur.fetchall()
        if len(rows) == 0:
            return "License key does not exists."

        query = "DELETE FROM license WHERE key = ?"
        param = (Key,)
        cur.execute(query, param)
        result = "License key has been successfully deleted."
    else:
        query = "DELETE FROM license"
        cur.execute(query)
        result = "All the license keys has been successfully deleted."

    conn.commit()
    conn.close()
    return result