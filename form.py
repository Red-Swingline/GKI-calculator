from tkinter import *
from db import *
import datetime
from tkinter import messagebox, simpledialog, ttk
from db import *
import datetime
import bcrypt
import matplotlib.pyplot as plt
import matplotlib.dates as dates


class User:
    """ Creates user and stores it in mysql database """

    def __init__(self, username, password, height, metric, mgdl, start_weight):
        self.username = username
        self.password = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt())
        self.height = height
        self.metric = metric
        self.mgdl = mgdl
        self.start_weight = start_weight

    def store_user(self):
        db.execute("INSERT INTO user (username, password, height, metric, mgdl, start_weight) VALUES(%s, %s, %s, %s, %s, %s)",
                   (self.username, self.password, self.height, self.metric, self.mgdl, self.start_weight))
        mydb.commit()


class Login:
    """ Login window """

    def __init__(self, master):
        self.master = master
        master.title('Login')
        self.master.geometry('350x350')

        self.upassword = StringVar()
        self.uname = StringVar()

        # Lables
        self.lable_username = Label(master, text="Username:")
        self.lable_username.place(x=25, y=75)
        self.lable_password = Label(master, text="Password:")
        self.lable_password.place(x=25, y=120)

        # Entry boxes
        self.username_entry = Entry(master, textvariable=self.uname)
        self.username_entry.place(x=110, y=75)
        self.password_entry = Entry(
            master, show="*", textvariable=self.upassword)
        self.password_entry.place(x=110, y=120)

        # Buttons
        self.login_button = Button(master, text='Login',
                                   width=7, bg="grey", command=lambda:
                                   self.password_check(self.username_entry.get(), self.password_entry.get()))
        self.login_button.place(x=70, y=200)
        self.reg_button = Button(master, text='Register',
                                 width=7, bg="grey", command=self.new_account)
        self.reg_button.place(x=160, y=200)
        self.cancelButton = Button(master, text='Cancel', width=7,
                                   bg="grey", command=quit)
        self.cancelButton.place(x=180, y=280)

    def password_check(self, username, password):
        """ Checks user input password with hash in DB"""
        db.execute(
            "SELECT user_id, password, metric, username FROM user WHERE username=%s", (username,))
        pw = db.fetchone()
        pword = pw[1]
        # This need some work as it barely works, at a min I need to add if username isnt int the return query.
        if bcrypt.checkpw(password.encode(), pword.decode().encode()):
            self.newWindow = Toplevel(self.master)
            self.app = Profile(self.newWindow, username, pw[0], pw[2])
            self.master.withdraw()
        else:
            wrong_login = messagebox.showerror(
                "Login", "Wrong username or password")

    def new_account(self):
        self.newWindow = Toplevel(self.master)
        self.app = Register(self.newWindow)
        self.master.withdraw()


class Profile:
    """ User profile """

    def __init__(self, master, username, user_id, metric):
        user_gki = db.execute(
            "SELECT DATE(rdate), ketones, glucose, round(((glucose)/(ketones)),2) AS gki FROM readings WHERE user_id=%s ORDER BY rdate DESC", (user_id,))
        rows = db.fetchall()
        self.master = master
        master.title(f'Profile for {username}')
        self.master.geometry('500x350')
        self.add_gki = Button(master, text='Add GKI',
                              width=7, bg="grey", command=lambda: self.addGKI(user_id))
        self.add_gki.place(x=70, y=70)
        self.gki_chart = Button(master, text='GKI Chart',
                                width=7, bg="grey", command=lambda: GKI_Chart(user_id))
        self.gki_chart.place(x=170, y=70)
        self.add_weight = Button(master, text='Add Weight',
                                 width=7, bg="grey", command=lambda: self.addweight(user_id))
        self.add_weight.place(x=270, y=70)
        self.weight_chart = Button(master, text='Weightr Chart',
                                   width=9, bg="grey", command=lambda: Weight_Chart(user_id))
        self.weight_chart.place(x=370, y=70)
        self.close_button = Button(master, text='close',
                                   width=7, bg="grey", command=quit)
        self.close_button.place(x=300, y=300)
        self.gki_table = ttk.Treeview(master, columns=(
            1, 2, 3, 4), show='headings', height=7)
        self.gki_table.place(x=70, y=110)

        self.gki_table.heading(1, text="Date Taken")
        self.gki_table.heading(2, text="ketones")
        self.gki_table.heading(3, text="Glucose")
        self.gki_table.heading(4, text="GKI")
        self.gki_table.column("#1", anchor="center", width=100, stretch=NO)
        self.gki_table.column("#2", anchor="center", width=75, stretch=NO)
        self.gki_table.column("#3", anchor="center", width=75, stretch=NO)
        self.gki_table.column("#4", anchor="center", width=75, stretch=NO)
        for i in rows:
            self.gki_table.insert('', 'end', values=i)

    def addGKI(self, user_id):
        self.newWindow = Toplevel(self.master)
        self.app = Add_gki(self.newWindow, user_id)

    def addweight(self, user_id):
        self.newWindow = Toplevel(self.master)
        self.app = Add_weight(self.newWindow, user_id)


class GKI_Chart:
    """ GKI line chart """

    def __init__(self, user_id):
        GKI_reading_query = db.execute(
            "SELECT ((glucose)/(ketones)) AS gki, rdate FROM readings WHERE user_id=%s ORDER BY rdate ASC LIMIT 5", (user_id,))
        result = db.fetchall()
        dates = []
        values = []
        for row in result:
            dates.append(row[1])
            values.append(row[0])
        plt.plot(dates, values, 'o-')
        plt.grid()
        plt.show()


class Weight_Chart:
    """ Weight line chart """

    def __init__(self, user_id):
        Weight_reading_query = db.execute(
            "SELECT weight, rdate FROM weight WHERE user_id=%s ORDER BY rdate ASC LIMIT 5", (user_id,))
        result = db.fetchall()
        dates = []
        values = []
        for row in result:
            dates.append(row[1])
            values.append(row[0])
        plt.plot(dates, values, 'o-')
        plt.grid()
        plt.show()


class Add_weight:
    """ Log new weight """

    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id
        master.title('Add Weight')
        self.master.geometry('500x200')
        heading = Label(master, text="Log Weight", fg="black",
                        bg="grey", width="500", height="3",)
        heading.pack()
        # Labels for entry boxes
        self.lable_weight = Label(master, text="New Weight:")
        self.lable_weight.place(x=15, y=75)

        self.weight = StringVar()

        # Entry boxes for ketones and Glucose
        self.weight_reading = Entry(master, textvariable=self.weight)
        self.weight_reading.place(x=120, y=75)
        self.add_button = Button(
            master, text="Add", width="7", bg="grey", command=self.save_weight)
        self.add_button.place(x=120, y=120)
        self.cancel_button = Button(
            master, text="Cancel", bg="grey", command=self.close)
        self.cancel_button.place(x=220, y=120)

    def save_weight(self):
        "Stores user-supplied data in the database"

        db.execute("INSERT INTO weight (user_id, weight, rdate) VALUES(%s, %s, %s)",
                   (self.user_id, self.weight.get(), datetime.datetime.now()))
        mydb.commit()
        self.master.destroy()

    def close(self):
        self.master.destroy()


class Add_gki:
    """Add New GKI reading"""

    def __init__(self, master, user_id):
        self.master = master
        master.title('Add GKI')
        self.master.geometry('500x350')
        heading = Label(master, text="Add GKI reading", fg="black",
                        bg="grey", width="500", height="3",)
        heading.pack()
        # Labels for entry boxes
        self.lable_ketones = Label(master, text="Ketones:")
        self.lable_ketones.place(x=15, y=75)
        self.lable_glucose = Label(master, text="Glucose:")
        self.lable_glucose.place(x=15, y=100)

        self.ket = StringVar()
        self.glu = StringVar()
        self.mgdl = IntVar()

        # Entry boxes for ketones and Glucose
        self.ketones_entry = Entry(master, textvariable=self.ket)
        self.ketones_entry.place(x=120, y=75)
        self.glucose_entry = Entry(master, textvariable=self.glu)
        self.glucose_entry.place(x=120, y=120)
        self.calculate_button = Button(
            master, text="Add", width="7", bg="grey", command=lambda: [self.gki_clicked(user_id), self.ketones_entry.delete(0, END), self.glucose_entry.delete(0, END)])
        self.calculate_button.place(x=150, y=180)
        self.close_readings_button = Button(
            master, text="Cancel", bg="grey", command=self.close)
        self.close_readings_button.place(x=250, y=180)

    def close(self):
        self.master.destroy()

    def ketone_level(self):
        "Returns the ketone level from the GUI as float"
        return float(self.ket.get())

    def glucose_level(self):
        "Returns the glucose level in mmol/L from the GUI as float"
        self.raw = float(self.glu.get())

        # If user selected a mg/dl checkbox, convert glucose to mmol/L
        if self.mgdl.get() == 1:
            return self.raw/18
        else:
            return self.raw

    def store_readings(self, user_id, ketone, glucose):
        "Stores user-supplied data in the database"

        db.execute("INSERT INTO readings (user_id, ketones, glucose, rdate) VALUES(%s, %s, %s, %s)",
                   (user_id, ketone, glucose, datetime.datetime.now()))
        mydb.commit()

    def gki_clicked(self, user_id):  # This need some work
        "Gets user input from database, runs the GKI calculation, stores result"
        ketone = self.ketone_level()
        glucose = self.glucose_level()

        self.store_readings(user_id, ketone, glucose)


class Register:
    """Registration window to allow users to be created and stored into the DB"""

    def __init__(self, master):
        self.master = master
        master.title('Create Account')
        self.master.geometry('500x750')
        heading = Label(master, text="Register a new account", fg="black",
                        bg="grey", width="500", height="3",)
        heading.pack()

        # Labels for entry boxes
        self.lable_username = Label(master, text="Username:")
        self.lable_username.place(x=25, y=75)
        self.lable_password = Label(master, text="Password:")
        self.lable_password.place(x=25, y=120)
        self.lable_height = Label(master, text="height:")
        self.lable_height.place(x=45, y=165)
        self.lable_weight = Label(master, text="Start Weight:")
        self.lable_weight.place(x=20, y=200)

        self.uname = StringVar()
        self.upassword = StringVar()
        self.height = IntVar()
        self.mgdl = IntVar()
        self.metric = IntVar()
        self.start_weight = StringVar()

        # Entry boxes for ketones and Glucose
        self.username_entry = Entry(master, textvariable=self.uname)
        self.username_entry.place(x=110, y=75)
        self.password_entry = Entry(
            master, show="*", textvariable=self.upassword)
        self.password_entry.place(x=110, y=120)
        self.height_entry = Entry(master, textvariable=self.height)
        self.height_entry.place(x=110, y=165)
        self.height_entry = Entry(master, textvariable=self.start_weight)
        self.height_entry.place(x=110, y=200)

        # Creates buttons.
        self.metric_checkbox = Checkbutton(
            master, text='Metric?', variable=self.metric)
        self.metric_checkbox.place(x=120, y=240)
        self.mgdl_checkbox = Checkbutton(
            master, text='Are you using mg/dL?', variable=self.mgdl)
        self.mgdl_checkbox.place(x=120, y=260)
        self.register_button = Button(master, text='Ok', width=7,
                                      bg="grey", command=self.reg_user)
        self.register_button.place(x=150, y=280)
        self.cancelButton = Button(
            master, text='Cancel', width=7,
            bg="grey", command=self.cancel_reg)
        self.cancelButton.place(x=250, y=280)

    def cancel_reg(self):
        self.master.destroy()
        main().app.deiconify

    def reg_user(self):
        """ Gets user input from registration from"""
        new_usr = User(self.uname.get(), str(self.upassword.get()), self.height.get(),
                       self.metric.get(), self.mgdl.get(), float(self.start_weight.get()))
        User.store_user(new_usr)
        self.master.destroy()
        main().app.deiconify


def main():
    root = Tk()
    app = Login(root)
    root.mainloop()


if __name__ == '__main__':
    main()
