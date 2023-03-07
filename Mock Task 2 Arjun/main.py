from flask import Flask, render_template, request, url_for , redirect , session
import sqlite3


import re
app = Flask(__name__)


app.secret_key="__privatekey__"

    

@app.route('/')
def home_Login():
    msg = ''
    return render_template('login.html')

@app.route('/home',methods=['POST','GET'])
def home():

            #email = request.form['addr']
            #password = request.form['pass']
        with sqlite3.connect("users.db") as con:
            cur = con.cursor()
            cur.execute("select * from users")
            #cur.execute ("select * from users WHERE addr = %s password = %s", (email, password,))

            
            
        return render_template('home.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/signup',methods=['POST','GET'])
def signup_form():
    
    con = sqlite3.connect('users.db')
    c=con.cursor()
    if request.method=='POST':
    
        name=request.form["name"]
        addr=request.form["addr"]
        password=request.form["password"]
        statment = f"SELECT * from users WHERE name='{name}' AND password='{password}';"
        c.execute(statment)
        data = c.fetchone
        print(data)
        if data == None:
            return render_template("error.html")
        else:
            c.execute("INSERT INTO users (name,addr,password) VALUES (?,?,?)",(name,addr,password))
            con.commit()
            con.close()
        return render_template('login.html',msg="done")
           
@app.route('/error')
def error():
    return render_template('error.html')
if __name__ == '__main__':
    app.run(debug=True)