import sqlite3

def connect():
    conn = sqlite3.connect("messaging.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXIsTS users (user_id INTEGER PRIMARY KEY,email varchar(20),password varchar(20),name varchar(20),address varchar(50),city varchar(30),state ,zip)")
    cur.execute("CREATE TABLE IF NOT EXISTS  messages (message_id INTEGER PRIMARY KEY,user_id int,recipient_id int,date_sent date,content text)")
    conn.commit()
    conn.close()

def insert(email,password,name,address,city,state,zip):
    conn = sqlite3.connect("messaging.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES(NULL,?,?,?,?,?,?,?)",(email,password,name,address,city,state,zip))
    conn.commit()
    conn.close()

def search(email,password):
    conn = sqlite3.connect("messaging.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=? and password=?",(email,password))
    rows = cur.fetchall()
    conn.close()
    return rows

def search_messages(message_id):
    conn = sqlite3.connect("messaging.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages WHERE message_id=?",(message_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def add_message(user_id,recipient_id,date_sent,content):
    conn = sqlite3.connect("messaging.db")
    cur = conn.cursor()
    cur.execute("Insert into messages values (NULL,?,?,?,?)",(user_id,recipient_id,date_sent,content))
    conn.commit()
    conn.close()


def insert_in_messages(user_id,recipient_id,date_sent,content):
    conn = sqlite3.connect("messaging.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO messages VALUES(NULL,?,?,?,?)",(user_id,recipient_id,date_sent,content))
    conn.commit()
    conn.close()


def display_user_posts(user_pk):
    conn = sqlite3.connect('messaging.db')
    cur = conn.cursor()
    cur.execute("Select * from messages where user_id={}".format(user_pk))
    rows = cur.fetchall()
    conn.close()
    return rows


def display_all_posts(recipient_id):
    conn = sqlite3.connect('messaging.db')
    cur = conn.cursor()
    cur.execute("Select * from messages where recipient_id=(Select email from users where user_id = {}) order by date_sent desc".format(recipient_id))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_message(message_id):
    conn = sqlite3.connect('messaging.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM messages where message_id={}".format(message_id))
    conn.commit()
    conn.close()