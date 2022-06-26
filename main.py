from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import ThreeLineIconListItem, IconLeftWidget
from db import *
import datetime


class MainApp(MDApp):
    def on_start(self):
        """Runs all on start methods, configurations ect"""
        # Checks if this is the first time the app has been run.
        frist_run = self.query_frun()
        if len(frist_run) == 0:
            self.message_output(
                "Welcome",
                "Please Enter your user infromation.",
            )
            self.root.ids.screen_manager.current = "info"

        else:
            self.set_info()
            self.gen_reading_list()
            self.root.ids.screen_manager.current = "readings"

    def gen_reading_list(self):
        """Generates reading list based on db query"""
        rows = self.get_readings()
        for r in rows:
            readings = ThreeLineIconListItem(
                text=f"Date: ",
                secondary_text=f"Glucose: {str(r[1])}                                  Keytones: {str(r[2])}",
                tertiary_text=f"GKI: {str(r[3])}",
            )
            gki = r[1]/r[2]
            if gki >= 9:
                readings.add_widget(
                    IconLeftWidget(icon="cancel")
                    )
            elif gki >= 6 and gki < 9:
                readings.add_widget(
                    IconLeftWidget(icon="checkbox-blank-circle-outline")
                    )
            elif gki >= 3 and gki < 6:
                readings.add_widget(
                    IconLeftWidget(icon="checkbox-blank-circle-outline")
                    ) 
            elif gki >= 1 and gki < 3:
                readings.add_widget(
                    IconLeftWidget(icon="checkbox-blank-circle-outline")
                    )     
            if gki >=9:
                readings.add_widget(
                    IconLeftWidget(icon="checkbox-blank-circle-outline")
                    )          
            self.root.ids.reading_list.add_widget(readings)

    def add_user_info(self, height, weight, age):
        frist_run = self.query_frun()
        if len(frist_run) == 0:
            self.insert_user_info(height, weight, age)
        else:
            self.update_user_info(height, weight, age)

    def insert_user_info(self, height, weight, age):
        """Inserts or updates table with user info from the form"""
        metric = self.root.ids.check_metric.state
        if metric == "normal":
            metric = False
        else:
            metric = True
        age = int(age.strip())
        height = height.strip()
        weight = float(weight.strip())
        db.execute(
            f"""INSERT INTO user_info(age, height, weight, metric) VALUES ('{age}', '{height}','{weight}','{metric}')"""
        )
        mydb.commit()
        self.insert_frist()

    def update_user_info(self, height, weight, age):
        metric = self.root.ids.check_metric.state
        if metric == "normal":
            metric = False
        else:
            metric = True
        age = int(age.strip())
        height = height.strip()
        weight = float(weight.strip())
        db.execute(
            f"""UPDATE user_info SET age = '{age}',
                    height = '{height}', weight = '{weight}', metric = '{metric}' WHERE id = 1; """
        )
        mydb.commit()

    def insert_frist(self):
        """This method inserts True into the first run table. The on start method will check this table for true if present."""
        try:
            db.execute(
                f"""INSERT INTO frun(
             first_run) VALUES
             ('{True}')"""
            )
        finally:
            mydb.commit()

    def set_info(self):
        """Sets User Info based on whats in the table"""
        info = self.get_user_info()
        self.root.ids.user_age.text = f"{info[0][1]}"
        self.root.ids.user_height.text = f"{info[0][2]}"
        self.root.ids.user_weight.text = f"{info[0][3]}"
        if info[0][4] == "True":
            self.root.ids.check_metric.state = "down"

    def add_reading(self, glu, key):
        """Adds glucose and keytones reading to the table"""

    def get_readings(self):
        """Returns all readings from table"""
        db.execute("""SELECT * from readings""")
        readings = db.fetchall()
        return readings

    def get_user_info(sefl):
        """Returns user info from the table"""
        db.execute("""SELECT * from user_info""")
        user_info = db.fetchall()
        return user_info

    def previous_screen(self):
        """Determins which screen the back arround in the screen topbar should change to"""

    def query_frun(self):
        db.execute("""SELECT * from frun""")
        frist_run = db.fetchall()
        return frist_run

    def message_output(self, title, message):
        """Creates a simple popup message to the user when required"""
        close_button = MDFlatButton(text="Close", on_release=self.close_dialog)
        self.dialog = MDDialog(
            title=f"{title}",
            text=f"{message}",
            size_hint=(0.7, 1),
            buttons=[close_button],
        )
        self.dialog.open()
        return self.dialog

    def close_dialog(self, obj):
        """Closes dialog boxes"""
        self.dialog.dismiss()


if __name__ == "__main__":
    ma = MainApp()
    ma.run()
