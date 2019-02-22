import kivy
kivy.require('1.10.1')

import time
from kivy.app import App
from kivy.lang import Builder
import os.path
from kivy.storage.jsonstore import JsonStore
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from plyer import accelerometer
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
import speech_recognition as sr
from audiostream import get_input

r = sr.Recognizer()
m = sr.Microphone()


class RecordButton(Button):
    # String Property to Hold output for publishing by Textinput
    output = StringProperty('')
    img = StringProperty('')

    def recognize(self, answer, dt):
        with m as source:
            audio = r.listen(source, phrase_time_limit=3)
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio, show_all = True)
            guesses = [d['transcript'] for d in value['alternative']]
            if answer in guesses:
                self.output = "Correct! You said \"{}\" ".format(answer)
            else:
                self.output = "Incorrect! You said \"{}\" \n \"{}\"".format(guesses[0], guesses)

        except sr.UnknownValueError:
            self.output = ("Oops! Didn't catch that")

        except sr.RequestError as e:
            self.output = ("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
        except TypeError:
            self.output = ("Uh oh! Try again!")


    def reload(self, figure):
        self.parent.parent.ids.img1.source = figure
        self.parent.parent.ids.img1.reload()

    def record(self):

        config = JsonStore("obj/speech.json")
        d = list(config.get('speech').items())
        import random
        ran = random.randint(0,4)
        answer = d[ran][0]
        figure = d[ran][1]
        self.reload(figure)
        from functools import partial
        Clock.schedule_once(partial(self.recognize, answer), 1)



class WelcomeScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class MotorScreen(Screen):
    def __init__(self, **kwargs):
        super(MotorScreen, self).__init__(**kwargs)
        self.sensorEnabled = False
        self.x_values = []
        self.y_values = []
        self.z_values = []

    def analyze_results(self):
        self.x_values = []
        self.y_values = []
        self.z_values = []


    def do_toggle(self):
        try:
            if not self.sensorEnabled:
                accelerometer.enable()
                Clock.schedule_interval(self.get_acceleration, 1 / 20.)
                self.sensorEnabled = True
                self.ids.toggle_button.disabled = True
                time.sleep(5)
                accelerometer.disable()
                Clock.unschedule(self.get_acceleration)
                self.sensorEnabled = False
                self.ids.toggle_button.disabled = False
                self.analyze_results()
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            status = "Accelerometer is not implemented for your platform"
            self.ids.accel_status.text = status

    def get_acceleration(self, dt):
        val = accelerometer.acceleration[:3]

        if not val == (None, None, None):
            self.ids.x_label.text = "X: " + str(val[0])
            self.ids.y_label.text = "Y: " + str(val[1])
            self.ids.z_label.text = "Z: " + str(val[2])
            self.x_values.append(val[0])
            self.y_values.append(val[1])
            self.z_values.append(val[2])

class SpeechScreen(Screen):
    pass

class ImageScreen(Screen):
    pass

class BasicEvalScreen(Screen):
    pass


class FillAbleTextInput(TextInput):
    def set_values_from_config(self):
        self.config_name = "obj/config.json"
        if os.path.isfile(self.config_name):
            config = JsonStore(self.config_name)
            if config.exists("user"):
                try:
                    self.text = config.get('user')[self.hint_text.lower()]
                except:
                    pass

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main.kv")


class MyApp(App):

    def __init__(self):
        App.__init__(self)
        self.config_name = "obj/config.json"


    def create_configuration(self):
        config = JsonStore(self.config_name)
        name = self.root.ids["welcome"].ids["name"].text
        lastname = self.root.ids["welcome"].ids["lastname"].text
        emergency = self.root.ids["welcome"].ids["emergency"].text
        config.put('user', name = name, lastname = lastname, emergency = emergency)

    def build(self):
        return presentation


if __name__ == '__main__':
    MyApp().run()