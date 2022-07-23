from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import ThreeLineIconListItem, IconLeftWidget
from db import *
from datetime import datetime


class MainApp(MDApp):
    def on_start(self):
        """Runs all on start methods, configurations ect"""
        # Checks if this is the first time the app has been run.
        create_tables()
        self.gen_reading_list()
        self.root.ids.screen_manager.current = "readings"

    def gen_reading_list(self):
        """Generates readings scrolling list based on db query"""
        rows = self.get_readings()
        for r in rows:
            readings = ThreeLineIconListItem(
                text=f"Date/Time:   {str(r[1])}",
                secondary_text=f"Glucose: {str(r[2])}                                  Keytones: {str(r[3])}",
                tertiary_text=f"GKI: {str(r[4])}",
                on_release=lambda x: self.delete_reading_clicked(r[0]),
            )
            gki = r[4]
            if gki > 9.0:
                readings.add_widget(
                    IconLeftWidget(
                        icon="cancel",
                        theme_text_color="Custom",
                        text_color=(245 / 255, 61 / 255, 39 / 255, 1),
                    )
                )
            elif 9.0 >= gki >= 6.0:
                readings.add_widget(
                    IconLeftWidget(
                        icon="speedometer-slow",
                        theme_text_color="Custom",
                        text_color=(245 / 255, 189 / 255, 39 / 255, 1),
                    )
                )
            elif 6.0 >= gki >= 3.0:
                readings.add_widget(
                    IconLeftWidget(
                        icon="speedometer-medium",
                        theme_text_color="Custom",
                        text_color=(245 / 255, 245 / 255, 39 / 255, 1),
                    )
                )
            elif 3.0 >= gki >= 1.0:
                readings.add_widget(
                    IconLeftWidget(
                        icon="speedometer",
                        theme_text_color="Custom",
                        text_color=(39 / 255, 245 / 255, 43 / 255, 1),
                    )
                )
            elif gki < 1.0:
                readings.add_widget(
                    IconLeftWidget(
                        icon="speedometer",
                        theme_text_color="Custom",
                        text_color=(39 / 255, 245 / 255, 43 / 255, 1),
                    )
                )
            self.root.ids.reading_list.add_widget(readings)

    def delete_reading_clicked(self, id):
        """Confirms that user want to delete reading then either dismisses dialog or deletes record"""
        self.dialog = MDDialog(
            text="Delete reading entry?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.close_dialog,
                ),
                MDFlatButton(
                    text="DELETE",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.delete_reading(
                        id,
                        self.dialog,
                    ),
                ),
            ],
        )
        self.dialog.open()

    def add_reading(self, glu, key):
        """Adds glucose and keytones reading to the table"""
        now = datetime.now()
        new_date = now.strftime("%d/%m/%Y %H:%M")
        test_value = self.value_test(glu, key)
        if test_value == True:
            new_glu = float(glu.strip())
            new_key = float(key.strip())
            gki = round(new_glu / new_key, 2)
            db.execute(
                f"""INSERT INTO readings(
                            glu, key, gki, r_date) VALUES
                            ('{new_glu}', '{new_key}', '{gki}', '{new_date}')"""
            )
            mydb.commit()
            self.clear_reading_input()
            self.root.ids.reading_list.clear_widgets()
            self.gen_reading_list()

    def value_test(self, glu, key):
        """Checks to see if user entered Value can be converted to a float"""
        g = ""
        k = ""
        try:
            glu1 = float(glu.strip())
            g = True
        except ValueError:
            self.message_output("Error", "Enter valid glucose value")
        try:
            key1 = float(key.strip())
            k = True
        except ValueError:
            self.message_output("Error", "Enter valid Keytone value")
        if g == True and k == True:
            return True

    def delete_reading(self, id, dialog):
        """Deletes reading the user selected from the scrolling reading list"""
        dialog.dismiss()
        db.execute(f"""DELETE FROM readings WHERE id = {id}""")
        mydb.commit()
        self.root.ids.reading_list.clear_widgets()
        self.gen_reading_list()

    def get_readings(self):
        """Returns all readings from table"""
        db.execute("""SELECT * from readings order by id DESC""")
        readings = db.fetchall()
        return readings

    def query_reading(self, id):
        """Returns all readings from table"""
        db.execute("""SELECT * from readings order by id DESC""")
        readings = db.fetchall()
        return readings

    def clear_reading_input(self):
        """Clears Glucose and Keytones text input values after inserted into table"""
        self.root.ids.user_glu.text = ""
        self.root.ids.user_key.text = ""

    def previous_screen(self):
        """Determins which screen the back arround in the screen topbar should change to"""
        # Place holder for new screens

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
