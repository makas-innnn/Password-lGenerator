from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard
import random
import string

def generate_strong_password(length):
    lo = random.choice(string.ascii_lowercase)
    up = random.choice(string.ascii_uppercase)
    di = random.choice(string.digits)
    sy = random.choice("!@#$%^&*")
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    rest = ""
    for i in range(length - 4):
        rest += random.choice(all_chars)
    combined = list(lo + up + di + sy + rest)
    for i in range(len(combined) - 1, 0, -1):
        j = random.randint(0, i)
        combined[i], combined[j] = combined[j], combined[i]
    return "".join(combined)

class PasswordApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text="Генератор паролей", font_size=24))
        
        self.pass_output = TextInput(text="", readonly=True, font_size=18, size_hint_y=None, height=50)
        layout.add_widget(self.pass_output)
        
        btn_gen = Button(text="Сгенерировать", font_size=18, size_hint_y=None, height=50)
        btn_gen.bind(on_press=self.generate)
        layout.add_widget(btn_gen)
        
        btn_copy = Button(text="Копировать", font_size=18, size_hint_y=None, height=50)
        btn_copy.bind(on_press=self.copy)
        layout.add_widget(btn_copy)
        
        return layout

    def generate(self, instance):
        self.pass_output.text = generate_strong_password(16)

    def copy(self, instance):
        if self.pass_output.text:
            Clipboard.copy(self.pass_output.text)

if __name__ == '__main__':
    PasswordApp().run()