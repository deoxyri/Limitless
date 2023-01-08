from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App, Builder
from kivy.core.window import Window

Builder.load_file("kivy_custom_file.kv")
# --- this changes the app's default background --- #
Window.clearcolor = (0, 0.6, 0.1, 1.0)
Window.size = (600, 400)


class User(Screen):
    pass

class RootWidget(ScreenManager):
    pass

class Test(App):

    def build(self):
        return RootWidget()

if __name__ == '__main__':
    Test().run()