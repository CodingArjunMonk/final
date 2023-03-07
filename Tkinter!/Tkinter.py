from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk,messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz


GUI = Tk()
GUI.title("Weather App")
GUI.geometry("900x500+300+200")
GUI.resizable(False,False)

GUI.config(background="pink")
#search box

def getWeather():
    try:
        city=textfield.get()

        geolocator=Nominatim(user_agent="geoapiExercises")
        location= geolocator.geocode(city)
        obj = TimezoneFinder()
        result=obj.timezone_at(lng=location.longitude,lat=location.latitude)

        home=pytz.timezone(result)
        local_time=datetime.now(home)
        current_time=local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

    #weather
        api="https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=bc8788fdf66d80fb56046be09bb73949"


        json_data = requests.get(api).json()
        condition = json_data["weather"][0]["main"]
        description = json_data["weather"][0]["description"]
        temp = int((json_data["main"]["temp"]-266.15) * 0.5)
        pressure = json_data["main"]["pressure"]
        humidity = json_data["main"]["humidity"]
        wind = json_data["wind"]["speed"]

        t.config(text=(temp,"º"))
        c.config(text=(condition,"!","FEELS","LIKE",temp,"Cº"))

        w.config(text=wind)
        h.config(text=humidity)
        d.config(text=description)
        p.config(text=pressure)

    except Exception as e:
        messagebox.showerror("Weather App","Invalid Entry!")

Search_image=PhotoImage(file="search.png")
myimage=Label(image=Search_image,bg="#ff00d1")
myimage.place(x=20,y=20)

textfield=tk.Entry(GUI,justify="center",width=17,font=("poppins",25,"bold"),bg="#ff00d1",border=0,fg="white")
textfield.place(x=50,y=40)
textfield.focus()

Search_icon=PhotoImage(file="search_icon.png")
myimage_icon= Button(image=Search_icon,borderwidth=0,cursor="hand2",bg="#404040",command=getWeather)
myimage_icon.place(x=400,y=34)

#logo
Logo_image = PhotoImage(file="logo.png")
logo = Label(image=Logo_image,bg="pink")
logo.place(x=150,y=100)

#bottom box
Frame_image=PhotoImage(file="box.png")
frame_myimage=Label(image=Frame_image,bg="pink")
frame_myimage.pack(padx=5,pady=5,side=BOTTOM)

#time
name=Label(GUI,font=("arial",15,"bold"))
name.place(x=30,y=100)
clock=Label(GUI,font=("Helvetica",20))
clock.place(x=30,y=130)

#LABEL
label1= Label(GUI,text="WIND",font=("Helvetica",15,"bold"),fg="white",bg="#1ab5ef")
label1.place(x=120,y=400)

label2= Label(GUI,text="HUMIDITY",font=("Helvetica",15,"bold"),fg="white",bg="#1ab5ef")
label2.place(x=225,y=400)

label3= Label(GUI,text="DESCRIPTION",font=("Helvetica",15,"bold"),fg="white",bg="#1ab5ef")
label3.place(x=430,y=400)

label4= Label(GUI,text="PRESSURE",font=("Helvetica",15,"bold"),fg="white",bg="#1ab5ef")
label4.place(x=650,y=400)

t=Label(font=("ariel",70,"bold"),fg="#ee666d")
t.place(x=400,y=150)
c=Label(font=("ariel",15,"bold"))
c.place(x=400,y=250)

w=Label(text="...",font=  ("ariel",20,"bold"),bg="#1ab5ef")
w.place(x=120,y=430)
h=Label(text="...",font=("ariel",20,"bold"),bg="#1ab5ef")
h.place(x=280,y=430)
d=Label(text="...",font=("ariel",20,"bold"),bg="#1ab5ef")
d.place(x=450,y=430)
p=Label(text="...",font=("ariel",20,"bold"),bg="#1ab5ef")
p.place(x=670,y=430)



GUI.mainloop()