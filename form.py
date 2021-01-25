from tkinter import * 
from db import *
from PIL import ImageTk,Image
from matplotlib import dates
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import datetime

def list_readings():
    "Queries mysql for GKI and reading dates, plots them on a line chart"
    list_reading_query = db.execute("SELECT ((glucose)/(ketones)) AS gki, rdate FROM readings WHERE user_id=1")
    result = db.fetchall()
    dates = []
    values = []
    for row in result:
        dates.append(row[1])
        values.append(row[0])
    plt.plot(dates,values,'o-')
    plt.grid() 
    plt.show()

def ketone_level():
    "Returns the ketone level from the GUI as float"
    return float(ket.get())

def glucose_level():
    "Returns the glucose level in mmol/L from the GUI as float"
    raw = float(glu.get())

    # If user selected a mg/dl checkbox, convert glucose to mmol/L
    if mgdl.get() == 1:
        return raw/18
    else:
        return raw

def display_gki(glucose, keytone):
    "Updates GUI with GKI calculation results"
    gki = glucose/ketone

    if gki <1:
        lvl = "You're in the highest therapeutic level ketosis."
    elif gki <=3:
        lvl = "You're in a high therapeutic level of ketosis."
    elif gki <=6:
        lvl = "You're in a moderate level of ketosis."
    elif gki <=9:
        lvl = "You're in a low level of ketosis."
    else:
        lvl = "You are not in ketosis"

    label_gki = Label(screen, text="Your GKI is: ")
    label_gki.place(x=12, y=240)
    label_round = Label(screen, text=round(gki,2)) # Rounds results to two decimal places
    label_round.place(x=90, y=240) 
    lable_lvl = Label(screen, text=lvl)
    lable_lvl.place(x=30, y=280)

def store_readings(user_id, ketone, glucose):
    "Stores user-supplied data in the database"

    db.execute("INSERT INTO readings (user_id, ketones, glucose, rdate) VALUES(%s, %s, %s, %s)",
        (user_id, ketone, glucose, datetime.datetime.now()))
    mydb.commit()

def gki_clicked():
    "Gets user input from database, runs the GKI calculation, stores result"
    ketone = ketone_level()
    glucose = glucose_level()

    user_id = 1 # This will get replaced when I add reg/login 

    store_readings(user_id, ketone, glucose)

    display_gki(glucose, keytone)

    ketones_entry.delete(0,END)
    glucose_entry.delete(0,END)


screen = Tk()
create_table()

# Creates the main from window
screen.geometry("500x350")
screen.title("GKI")
heading = Label(text="Calculate your GKI", fg = "black", bg = "grey", width="500", height="3",)
heading.pack()

# Labels for entry boxes
lable_ketones = Label(text = "Ketones:")
lable_ketones.place(x = 15, y=75)
lable_glucose = Label(text = "Glucose:")
lable_glucose.place(x = 15, y=100)

ket = StringVar() 
glu = StringVar()
mgdl = IntVar()

# Entry boxes for ketones and Glucose
ketones_entry = Entry(screen, textvariable = ket)
ketones_entry.place(x=120, y=75) 
glucose_entry = Entry(screen, textvariable = glu)
glucose_entry.place(x=120, y=120)

# Creates buttons.
mgdl_checkbox = Checkbutton(screen, text= "Are you using mg/dL?", variable=mgdl)
mgdl_checkbox.place(x= 120, y= 150)
calculate_button = Button(screen, text = "Calculate", width= "7", bg = "grey", command = gki_clicked)
calculate_button.place(x= 150, y=180)
list_readings_button = Button(screen, text="Pull Readings", bg= "grey", command=list_readings)
list_readings_button.place(x= 250, y= 180)

screen.mainloop()