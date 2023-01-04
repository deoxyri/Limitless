# ----------------------------------------------------------------------------------------------------------------------
# KIVY - GUI
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
# ----------------------------------------------------------------------------------------------------------------------
# APP - CLASS SETUP
class ImiKami(App):
    def build(self):
        self.window = GridLayout()
        # self.window.rows = 6
        self.window.cols = 1
        # self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"centre_x": 0.5, "centre_y": 0.5}
        # --------------------------------------------------------------------------------------------------------------
        #LAYOUT
        # layout = FloatLayout()
        # add widgets to window
        # --------------------------------------------------------------------------------------------------------------
        # Image Widget
        self.window.add_widget(Image(source="kinect.png"))
        # --------------------------------------------------------------------------------------------------------------
        # Label Widget
        self.greeting = Label(text="Welcome to the Training Session",
                              font_size=18,
                              font_name = 'Times.ttf',
                              color='#00FFCE'
                              )
        self.window.add_widget(self.greeting)
        # --------------------------------------------------------------------------------------------------------------
        # User Input Text
        self.user = TextInput(multiline=False,
                              padding_y=(20, 20),
                              size_hint=(1, 1)
                              )
        self.window.add_widget(self.user)
        # --------------------------------------------------------------------------------------------------------------
        # Button Widget
        # layout_buttons = BoxLayout(orientation = "vertical")
        # self.window.cols = 2
        self.button1 = Button(text="Confirm",
                              font_name='Times.ttf',
                             size_hint=(0.5, 1),
                             bold=True,
                             background_color='#AF88DF',
                             background_normal="",
                            center= (1,1)
                             )
        self.button1.bind(on_press=self.callback)

        self.button2 = Button(text="Exit",
                              font_name='Times.ttf',
                             size_hint=(0.5, 1),
                             bold=True,
                             background_color='#AF88DF',
                             background_normal="",
                              center=(5, 1)
                             )
        self.button2.bind(on_press=self.callback)

        # layout_buttons.add_widget(self.button1)
        # layout_buttons.add_widget(self.button2)

        self.window.add_widget(self.button1)
        self.window.add_widget(self.button2)
        # --------------------------------------------------------------------------------------------------------------
        #DROP DOWN MENU
        drop_down = DropDown()
        for index in range(15):
            # now, Add the button in the drop down list
            drop_button = Button(text='List % d' % index, size_hint_y=None, height=30)

            # now we will bind the button for showing the text when it is selected
            drop_button.bind(on_release=lambda btton: drop_down.select(btton.text))

            # then we will add the button inside the drop_down list
            drop_down.add_widget(drop_button)

            # now we will create the big main button
        main_button = Button(text='MAIN', size_hint=(None, None), pos=(350, 300))

        # now, we will first show the drop_down menu when the main button will releases
        # we should note that all of the bind() function calls will pass the instance of the caller
        # as the first argument of the callback (in this program, the main_button instance)
        # now, dropdown.open.
        main_button.bind(on_release=drop_down.open)

        # now we have to do last thing, listen for the selection in the
        # dropdown list and assign the data to the button text.
        drop_down.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))

        # runtouchApp:
        # If we pass only the widget in runtouchApp(), the Window will be
        # created and our widget will be added to that window as the root widget.
        self.window.add_widget(main_button)
        # runTouchApp(main_button)
        # --------------------------------------------------------------------------------------------------------------
        return self.window
        # --------------------------------------------------------------------------------------------------------------
    def callback(self, instance):
        self.greeting.text = "You have selected: " + self.user.text

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    ImiKami().run()
# ----------------------------------------------------------------------------------------------------------------------