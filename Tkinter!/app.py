from geopy.geocoders import Nominatim
from tkinter import ttk,messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from flask import Flask, render_template, request, url_for , redirect , session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/search')
def search_Weather():
    return render_template('search.html')
def getWeather():
    try:
        city= "Solihull"

        geolocator=Nominatim(user_agent="geoapiExercises")
        location= geolocator.geocode(city)
        obj = TimezoneFinder()
        result=obj.timezone_at(lng=location.longitude,lat=location.latitude)

        home=pytz.timezone(result)
        local_time=datetime.now(home)
        current_time=local_time.strftime("%I:%M %p")


    #weather
        api="https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=bc8788fdf66d80fb56046be09bb73949"


        json_data = requests.get(api).json()
        condition = json_data["weather"][0]["main"]
        description = json_data["weather"][0]["description"]
        temp = int((json_data["main"]["temp"]-266.15) * 0.5)
        pressure = json_data["main"]["pressure"]
        humidity = json_data["main"]["humidity"]
        wind = json_data["wind"]["speed"]
        print(json_data)
        print(condition,description,temp,pressure,humidity,wind)
    except:
        print("City doesnt exist")
getWeather()

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
        if data == None:#checking if exist already
            return render_template("error.html")
        else:
            c.execute("INSERT INTO users (name,addr,password) VALUES (?,?,?)",(name,addr,password))
            con.commit()
            con.close()
        return render_template('login.html',msg="done")
    

@app.route('/login', methods=["POST","GET"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form["password"]



    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)


