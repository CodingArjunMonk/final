#app.py
from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
 

conn = sqlite3.connect('users.db')
@app.route('/')
def demohome():
    return render_template('demohome.html')
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
    
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('demohome'))
 
@app.route('/login/', methods=['GET', 'POST'])
def login():
    con = sqlite3.connect('users.db')
    c=con.cursor()
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)
        
        
        # Check if account exists using MySQL
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        # Fetch one record and return result
        account = c.fetchone()
        print(account)
        if account:
            password_rs = account[3]
            print(type(password_rs))
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[2]
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
 
    return render_template('login.html')
  
@app.route('/register', methods=['GET', 'POST'])
def register():
    con = sqlite3.connect('users.db')
    c = con.cursor()
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    
        _hashed_password = generate_password_hash(password)
        
        #Check if account exists using MySQL
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        account = c.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            c.execute("INSERT INTO users (fullname, username, password, email) VALUES (?,?,?,?)", (fullname, username, _hashed_password, email))
            con.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')
   
   
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('demohome'))
  
@app.route('/profile')
def profile(): 
    con = sqlite3.connect('users.db')
    c=con.cursor()
    # Check if user is loggedin
    if 'loggedin' in session:
        c.execute('SELECT * FROM users WHERE id = ?',[session['id']])
        account = c.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('demohome'))
 
if __name__ == "__main__":
    app.run(debug=True)