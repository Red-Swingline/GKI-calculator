from tkinter import * 
from db import *
from PIL import ImageTk,Image
from matplotlib import dates
import numpy as np
import matplotlib.pyplot as plt
import datetime


screen = Tk()
create_table()

def list_readings():
    list_reading_query = db.execute("SELECT ((glucose)/(ketones)) AS gki FROM readings WHERE user_id=1")
    result = db.fetchall()
    plt.plot(result)
    plt.grid()
    plt.show()

    
    # This will get the user input and run the GKI calculation 
def gki(): 
    k = float(ket.get()) 
    g = float(glu.get()) 
    m = mgdl.get()
    d = datetime.datetime.now()  
    u = 1 # Hard coded user_ID for readings table this will get replaced when I add reg/login 

    if m == 1: # Converts glucose to mmol/L if user selected a mg/dl checkbox
        g = g/18
        results = g/k 
    else:
        results = g/k
    if results <1:
        lvl = "You're in the highest therapeutic level ketosis."
    elif results <=3:
        lvl = "You're in a high therapeutic level of ketosis."
    elif results <=6:
        lvl = "You're in a moderate level of ketosis."
    elif results <=9:
        lvl = "You're in a low level of ketosis."
    else:
        lvl = "You are not in ketosis"
    sql_command = "INSERT INTO readings (user_id, ketones, glucose, rdate) VALUES(%s, %s, %s, %s)"
    values = (u, k, g, d)
    db.execute(sql_command,values)
    mydb.commit()
    label_gki = Label(screen, text="Your GKI is: ")
    label_gki.place(x=12, y=240)
    label_round = Label(screen, text=round(results,2)) # Rounds results to two decimal places
    label_round.place(x=90, y=240) 
    lable_lvl = Label(screen, text=lvl)
    lable_lvl.place(x=30, y=280)
    ketones_entry.delete(0,END)
    glucose_entry.delete(0,END)

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
calculate_button = Button(screen, text = "Calculate", width= "7", bg = "grey", command = gki)
calculate_button.place(x= 150, y=180)
list_readings_button = Button(screen, text="Pull Readings", bg= "grey", command=list_readings)
list_readings_button.place(x= 250, y= 180)

screen.mainloop()