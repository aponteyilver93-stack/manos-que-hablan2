from kivy.app import App
from kivy.uix.label import Label


class Prueba(App):
    def build(self):
        return Label(text="Manos que hablan\nprueba lista", font_size="28sp")


Prueba().run()
