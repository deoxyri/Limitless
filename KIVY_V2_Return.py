# KIVY - GUI
# ----------------------------------------------------------------------------------------------------------------------
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App, Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty
# ----------------------------------------------------------------------------------------------------------------------
# DATABASE
from google.cloud.sql.connector import Connector, IPTypes
import os
import sqlalchemy
# ----------------------------------------------------------------------------------------------------------------------
# SETTING RECURSIVE LIMIT
import sys

sys.setrecursionlimit(10 ** 9)
print(sys.getrecursionlimit())
# ----------------------------------------------------------------------------------------------------------------------
# DATABASE CONNECTION FUNCTION
# ----------------------------------------------------------------------------------------------------------------------
# CREATE CONNECTION
# ----------------------------------------------------------------------------------------------------------------------
os.system("gcloud auth application-default login")
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\PC-User\AppData\Roaming\gcloud\application_default_credentials.json"

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "X:\Limitless\A - Skeletal Tracking\Keys\service_key_gcloud.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "F:\Limitless\Programs\Keys\service_key_gcloud.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_key_gcloud.json"

# credentials = google.oauth2.service_account.Credentials.from_service_account_file(
#     './Peepl-cb1dac99bdc0.json',
#     scopes=['https://www.googleapis.com/auth/cloud-platform'])


INSTANCE_CONNECTION_NAME = f"applied-craft-372501:australia-southeast2:imikami-demo-v1"
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
DB_USER = "postgres"
DB_PASS = "Limitless@96"
DB_NAME = "postgres"

# Initialize Connector Object
connector = Connector()


# function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
        enable_iam_auth=True
    )
    return conn


# ----------------------------------------------------------------------------------------------------------------------
# WRITING DATA INTO DATABASE
# ----------------------------------------------------------------------------------------------------------------------
# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)
# ----------------------------------------------------------------------------------------------------------------------
table_name_query = """SELECT table_name
FROM information_schema.tables
WHERE table_type='BASE TABLE'
AND table_schema='public'"""

# connect to connection pool
with pool.connect() as db_conn:
    table_names = db_conn.execute(table_name_query).fetchall()

# EXTRACTING UNIQUE EXERCISE NAMES FROM DATA TABLES
table_names.sort()
drop_down_data = (table_names[0:len(table_names) // 20])
exercises = []
# print(exercises)
print(drop_down_data)

for strings in drop_down_data:
    strings = list(strings)
    strings = ' '.join([str(elem) for elem in strings])

    exercise_name = strings.replace("head_data_", "")
    exercise_name = exercise_name.replace("head_data", "SELECT FROM BELOW")
    exercise_name = exercise_name.replace("_", " ")
    exercises.append(exercise_name)

# CAPITALISING FIRST LETTER - FOR A BETTER UI/UX
exercises = [x.title() for x in exercises]
# print(exercises)
# ----------------------------------------------------------------------------------------------------------------------
# WHITE BACKGROUND
Window.clearcolor = (1, 1, 1, 1)


# ----------------------------------------------------------------------------------------------------------------------
# APP - CLASS SETUP
class ImiKami(App):
    def build(self):
        self.window = GridLayout(orientation='tb-lr')
        self.window.cols = 1
        self.window.size_hint = (1, 1)
        self.window.pos_hint = {"centre_x": 0.5, "centre_y": 0.5}
        sm = ScreenManager()
        # --------------------------------------------------------------------------------------------------------------
        # LAYOUT
        # layout = FloatLayout()
        # add widgets to window
        # --------------------------------------------------------------------------------------------------------------
        # Image Widget
        self.window.add_widget(Image(source="Logo Sample 3.png"))
        # --------------------------------------------------------------------------------------------------------------
        # Label Widget
        self.greeting = Label(text="Welcome to the Training Session",
                              font_size=24,
                              font_name='Times.ttf',
                              color='#00000',
                              pos_hint={"center_x": 0.5, "center_y": 0.5}
                              )
        self.window.add_widget(self.greeting)
        # --------------------------------------------------------------------------------------------------------------
        # User Input Text
        # self.user = TextInput(multiline=False,
        #                       padding_y=(20, 20),
        #                       size_hint=(1, 1)
        #                       )
        # self.window.add_widget(self.user)
        # --------------------------------------------------------------------------------------------------------------
        # DROP DOWN MENU
        self.drop_down = DropDown()
        for index in exercises:
            # now, Add the button in the drop-down list
            self.drop_button = Button(text='%s' % index, size_hint_y=None, height=30)

            # now we will bind the button for showing the text when it is selected
            self.drop_button.bind(on_release=lambda btton: self.drop_down.select(btton.text))

            # then we will add the button inside the drop_down list
            self.drop_down.add_widget(self.drop_button)

            # now we will create the big main button
        self.main_button = Button(text='MENU', pos_hint={"center_x": 0.5, "center_y": 0.5})

        # now, we will first show the drop_down menu when the main button will releases
        # we should note that all of the bind() function calls will pass the instance of the caller
        # as the first argument of the callback (in this program, the main_button instance)
        # now, dropdown.open.
        self.main_button.bind(on_release=self.drop_down.open)

        # now we have to do last thing, listen for the selection in the
        # dropdown list and assign the data to the button text.
        self.drop_down.bind(on_select=lambda instance, x: setattr(self.main_button, 'text', x))

        # runtouchApp:
        # If we pass only the widget in runtouchApp(), the Window will be
        # created and our widget will be added to that window as the root widget.

        self.window.add_widget(self.main_button)
        # runTouchApp(main_button)

        # --------------------------------------------------------------------------------------------------------------
        # Button Widget
        # CONFIRM / EXIT BUTTONS
        h_layout = BoxLayout()

        button_confirm = Button(
            text="CONFIRM",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        button_confirm.bind(on_press=self.callback)

        button_exit = Button(
            text="EXIT",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        button_exit.bind(on_press=self.close_application)

        h_layout.add_widget(button_confirm)
        h_layout.add_widget(button_exit)

        self.window.add_widget(h_layout)
        # --------------------------------------------------------------------------------------------------------------
        return self.window

    def callback(self, instance):
        if __name__ == '__main__':
            self.greeting.text = "You have selected:" + self.main_button.text
            ex_name = self.main_button.text
            print(ex_name)
            return self.main_button.text

    def close_application(self, instance):
        # closing application
        App.get_running_app().stop()
        # removing window
        Window.close()

    # def go(self):
    #     os.execlp(sys.executable, 'python', 'KIVY_V1.py')


# ----------------------------------------------------------------------------------------------------------------------
# method which will render our application
if __name__ == "__main__":
    ImiKami().run()
# ----------------------------------------------------------------------------------------------------------------------
