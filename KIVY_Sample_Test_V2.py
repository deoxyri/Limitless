import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.image import Image

Config.set('graphics', 'resizable', '0')

# Designate Our .kv design file
Builder.load_string('''
<MyLayout>
   hassanGIF: hassanGIF
   BoxLayout:
      orientation: "vertical"
      size: root.width, root.height
      Label:
         # font_name: "files/cambriab.ttf"
         id: name_label
         text: "If you had 530M dinars, what would you do with it?"
         font_size: 32
      Button:
         id: my_button
         size_hint: .4, .2
         font_size: 32
         # font_name: "files/cambriaz.ttf"
         text: "Make me rich!"
         pos_hint: {'center_x': 0.5}
         background_color: 5/255,225/255,120/255,1
         on_press: root.press(self)
         # below functions are moved to the press() method
         # on_press: hassanGIF.anim_delay = 1/50
         # on_press: hassanGIF._coreimage.anim_reset(True)
         on_release: root.release(self)
         Image:
            id: hassanGIF
            source: 'files/sequence.zip'
            anim_delay : -1
            anim_loop: 1
            center_x: self.parent.center_x
            center_y: self.parent.center_y+400
            size: root.width-400, root.height-400
''')


class MyLayout(Widget):
    hassanGIF = Image()

    def release(self, my_button):
        print(f"Release: {my_button}")
        self.ids.my_button.background_color = 5 / 255, 225 / 255, 120 / 255, 1
        self.ids.my_button.color = 1, 1, 1, 1

    def press(self, my_button):
        print(f"\npress {my_button}")
        # Create variables for our widget
        # Update the label
        deck = list(range(1, 43))
        random.shuffle(deck)
        # Create list of 6 values, and assign each with a number between 1 and 42
        random_numbers = [0, 1, 2, 3, 4, 5]
        for i in range(0, 6):
            random_numbers[i] = deck.pop()

        # Sort the array from lowest to highest
        random_numbers.sort()
        self.ids.my_button.background_color = 50 / 255, 225 / 255, 120 / 255, 1
        self.ids.my_button.color = 180 / 255, 180 / 255, 180 / 255, 1

        self.ids.name_label.text = f'{random_numbers[0]}    ' \
                                   f'{random_numbers[1]}    ' \
                                   f'{random_numbers[2]}    ' \
                                   f'{random_numbers[3]}    ' \
                                   f'{random_numbers[4]}    ' \
                                   f'{random_numbers[5]}'

        self.hassanGIF.anim_delay = 1/50
        print(self.hassanGIF)
        if self.hassanGIF._coreimage:
            self.hassanGIF._coreimage.anim_reset(True)


class AwesomeApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    AwesomeApp().run()