import sqlite3
#creating all the tables for the database
def create_tables():
    conn = sqlite3.connect('Study2watch.db')
    cursor = conn.cursor()
 #tables made
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY, 
            username TEXT NOT NULL,
            password TEXT NOT NULL)''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            sessID TEXT PRIMARY KEY,
            id TEXT,
            showwatched TEXT,
            numofcycles INTEGER,
            cyclelength INTEGER,
            topicstudied TEXT,
            FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE
            )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS planner (
            topicsplanned TEXT,
            showlist TEXT,
            date TEXT,
            id TEXT,
            FOREIGN KEY (id) REFERENCES users(id)
            PRIMARY KEY (id, date, topicsplanned, showlist)
            )''') 

    conn.commit()
    conn.close()
#insertion of data for the signup/login page
def insertaccountdata(id, username, password):
    conn = sqlite3.connect('Study2watch.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (id, username, password) VALUES (?,?,?)', (id, username, password))
    conn.commit()
    conn.close()

#function to verify if user account has already been made based off id, username and password
def verify_user(id, username, password):
    conn = sqlite3.connect('Study2watch.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE id=? AND username=? AND password=?', (id, username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

#function to verify user by id, all users have unique ids
def idcheck(id):
    conn = sqlite3.connect('Study2watch.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE id=?', (id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None
#function to verify user by username alongside id like above, all users have unique id and username
def usernamecheck(username):
    conn = sqlite3.connect('Study2watch.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE username=?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

#insertion of data for the sessions page
def insertsessiondata(sessID, id, showwatched, numofcycles, cyclelength, topicstudied):
    conn = sqlite3.connect('Study2watch.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sessions (sessID, id, showwatched, numofcycles, cyclelength, topicstudied) VALUES (?, ?, ?, ?, ?, ?)', (sessID, id, showwatched, numofcycles, cyclelength, topicstudied))
    conn.commit()
    conn.close()

#function to verify if sessions are already made
def verify_sessID(sessID):
    conn = sqlite3.connect('Study2watch.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM sessions WHERE sessid=?', (sessID,))
    count = cursor.fetchone()
    conn.close()
    # indicates session is either in or out of database
    return count [0] > 0

#verifies session data based off users
def verify_session_data(id):
    conn = sqlite3.connect('Study2watch.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sessions WHERE id=?', (id,))
    sessions = cursor.fetchall()
    conn.close()
    return sessions

# gets the shows from sessions based off users
def getshowdata(id):
    conn = sqlite3.connect('Study2watch.db')
    cursor = conn.cursor()
    cursor.execute('SELECT showwatched FROM sessions WHERE id = ?', (id,))
    shows = cursor.fetchall()
    conn.close()
    return shows

def getsessiondata(id):
    conn = sqlite3.connect('Study2watch.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sessions WHERE id = ?', (id,))
    shows = cursor.fetchall()
    conn.close()
    return shows

def inserttimetabledata(id,date,topicsplanned,showlist):
    conn = sqlite3.connect('Study2watch.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO planner (id, date, topicsplanned, showlist) VALUES (?, ?, ?, ?)', (id, date, topicsplanned, showlist))
    conn.commit()
    conn.close()

def updatetimetabledata(id,date,topicsplanned,showlist):
    conn = sqlite3.connect('Study2watch.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE planner SET topicsplanned = ?, showlist = ? WHERE id = ? AND date = ?',(topicsplanned, showlist,id, date))
    conn.commit()
    conn.close()


def gettimetabledata(id,date):
    conn = sqlite3.connect('Study2watch.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM planner WHERE id = ? AND date=?', (id,date))
    planner = cursor.fetchone()
    conn.close()
    return planner


create_tables()