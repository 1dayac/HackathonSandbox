import kivy
kivy.require('1.10.1')


from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.uix.textinput import TextInput

class InterfaceManager(BoxLayout):

    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        self.forms = {}

        self.btn1 = Button(text='Touch screen to begin')
        self.btn1.bind(on_press=self.uniCallback)

        self.btn2 = Button(text='Speech function')
        self.btn2.bind(on_press=self.uniCallback)

        self.btn3 = Button(text='Motor function')
        self.btn3.bind(on_press=self.uniCallback)

        self.btn4 = Button(text='Face recognition')
        self.btn4.bind(on_press=self.uniCallback)

        self.lbl5 = Label(text='Here goes motor funtion')
        self.lbl5.bind(on_hover=self.uniCallback)


        self.add_widget(self.btn1)
        self.add_form("Speech function", self.btn1)
        self.add_form("Motor function", self.lbl5)
        self.add_form("Face recognition", self.btn1)

        self.add_form("Touch screen to begin", self.btn2)
        self.add_form("Touch screen to begin", self.btn3)
        self.add_form("Touch screen to begin", self.btn4)

        self.add_form("Here goes motor funtion", self.btn2)
        self.add_form("Here goes motor funtion", self.btn3)
        self.add_form("Here goes motor funtion", self.btn4)


    def add_form(self, key, form):
        if key not in self.forms:
            self.forms[key] = []
        self.forms[key].append(form)

    def uniCallback(self, button):
        self.clear_widgets()
        for widget in self.forms[button.text]:
            self.add_widget(widget)


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Button(text='Motor Function'))
        self.add_widget(Button(text='Face Function'))
        self.add_widget(Button(text='Voice Function'))

class MyApp(App):

    def build(self):
        manager = InterfaceManager(orientation='vertical')
        return manager

if __name__ == '__main__':
    MyApp().run()