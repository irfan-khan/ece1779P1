from flask import render_template, session, request, redirect, url_for
from app import webapp
import hashlib
import uuid
import mysql.connector

#import hashlib, uuid
import random

webapp.secret_key = '\x80\xa9s*\x12\xc7x\xa9d\x1f(\x03\xbeHJ:\x9f\xf0!\xb1a\xaa\x0f\xee'

@webapp.route('/login',methods=['GET','POST'])
def login():
    return render_template("example6_login.html")

@webapp.route('/login_submit',methods=['POST'])
def login_submit():
    print(request.form['username'])
    password = request.form['password']
    print(password)
    #hash password
    salt = uuid.uuid4().hex
    print("salt: " +  salt)
    hash_object = hashlib.sha1(password.encode('utf-8')+salt.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    print(hex_dig) #hashed password
    if 'username' in request.form and \
       request.form['username'] == 'spy' and \
       'password' in request.form and \
       request.form['password'] == 'secret':
        session['authenticated'] = True
        return redirect(url_for('sensitive'))

    return redirect(url_for('login'))


secrets = ["Wax on, wax off. Wax on, wax off",
           "I love the smell of napalm in the morning",
           "Hello, my name is Inigo Montoya. You killed my father. Prepare to die",
           "Here’s lookin’ at you, kid"
           ]


@webapp.route('/secure/index',methods=['GET','POST'])
def sensitive():
    if 'authenticated' not in session:
        return redirect(url_for('login'))

    secret = secrets[random.randint(0,len(secrets)-1)]
    
    return render_template("example6_secret.html",secret=secret)

@webapp.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('sensitive'))



@webapp.route('/login_v2',methods=['GET','POST'])
def login_v2():
    uname = None
    e = None
    
    if 'username' in session: 
        uname = session['username']
     
    if 'error' in session:
        e = session['error']
        
    return render_template("example6_login_v2.html",error=e,username=uname)

@webapp.route('/login_submit_v2',methods=['POST'])
def login_submit_v2():
    
    
    if 'username' in request.form and \
       request.form['username'] == 'spy' and \
       'password' in request.form and \
       request.form['password'] == 'secret':
        session['authenticated'] = True
        return redirect(url_for('sensitive'))
    
    if 'username' in request.form:
        session['username'] = request.form['username'] 

    session['error'] = "Error! Incorrect username or password!"

    return redirect(url_for('login_v2'))

def db_add_user(user, password):
    cnx = mysql.connector.connect(user='root', password='password',
                                  host='127.0.0.1',
                                  database='A1')
    cursor = cnx.cursor()

    query = "SELECT username FROM users WHERE username = '%s'" % (user)

    cursor.execute(query)
    user_exists = cursor.fetchall()
    if not user_exists:
        print("Username Available\nAdding Username: %s\nPassword: %s\n" % (user, password))
        add_user = ("INSERT INTO users (username, userpass,loggedin) VALUES ('%s','%s',1)" % (user, password))
        cursor.execute(add_user)
    else:
        print("User: %s already exists" % (user_exists[0]))
    cnx.commit()
    cursor.close()
    cnx.close()