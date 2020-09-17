from flask import Flask,render_template, request,redirect, session
import backend
import os
from datetime import date
import shutil

app = Flask(__name__)
app.secret_key = os.urandom(24)

backend.connect()

def get_fname(s):
    
    n = ''
    for char in s:
        if char!=' ':
            n+=char
        elif char==' ':
            break
    return n


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():
    data = request.form.to_dict()
    rows = backend.search(data['email'],data['password'])
    if len(rows)>=1:
        return redirect('/')
    else:
        backend.insert(data['email'],data['password'],data['name'],data['address'],data['city'],data['state'],data['zip'])
        return redirect('/index.html')

@app.route('/login',methods=['POST'])
def login():
    data = request.form.to_dict()
    rows = backend.search(data['email'],data['password'])
    if len(rows)==1:
        session['user_id'] = get_fname(rows[0][3])
        session['user_pk'] = rows[0][0]
        session['user_email'] = rows[0][1]
        return redirect('/dashboard.html')
    else:
        return redirect('/')


@app.route('/dashboard.html')
def dashboard():
    if 'user_id' in session:
        data = backend.display_all_posts(session['user_pk'])
        return render_template('dashboard.html',pk=session['user_pk'],name=session['user_id'],data=data)
    else:
        return redirect('/index.html')

@app.route('/logout',methods=['POST'])
def logout():
    session.pop('user_id')
    session.pop('user_pk')
    session.pop('user_email')
    return redirect('/index.html')

@app.route('/newmessage.html')
def opennewpost():
    if 'user_id' in session:
        return render_template('newmessage.html',name=session['user_id'])
    else:
        return redirect('/index.html')


@app.route('/sendamessage',methods=['POST'])
def addpost():
    data = request.form.to_dict()
    backend.insert_in_messages(session['user_pk'],data['emaddress'],date.today(),data['text'])
    return redirect('/viewall.html')


@app.route('/viewall.html')
def viewall():
    data = backend.display_user_posts(session['user_pk'])
    if 'user_id' in session:
        return render_template('viewall.html',data=data,name=session['user_id'])
    else:
        return redirect('/index.html')

@app.route('/viewthispost/<int:message_id>',methods=['POST'])
def view(message_id):
    message = backend.search_messages(message_id)
    if 'user_id' in session:
        return render_template('viewthispost.html',message=message)
    else:
        return render_template('/')

@app.route("/deletepost/<int:message_id>",methods=['POST'])
def delete(message_id):
    backend.delete_message(message_id)
    return redirect("/viewall.html")


app.run(debug=True)