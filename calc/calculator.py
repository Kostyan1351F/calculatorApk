import os
import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.resources import resource_add_path

import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("../.."), relative_path)


DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db")
DB_PATH = os.path.join(DB_DIR, "calc_history.db")


def db_connect():
    os.makedirs(DB_DIR, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = db_connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_record(expression: str):
    conn = db_connect()
    conn.execute("INSERT INTO history (expression) VALUES (?)", (expression,))
    conn.commit()
    conn.close()


def load_records():
    conn = db_connect()
    rows = conn.execute(
        "SELECT id, expression FROM history ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return rows


def clear_records():
    conn = db_connect()
    conn.execute("DELETE FROM history")
    conn.commit()
    conn.close()


class CalculatorRoot(Screen):
    display = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first_number = None
        self.operation = None
        self.new_number = True

    def on_button_press(self, instance):
        text = instance.text
        display = self.ids.display

        if text in '0123456789.':
            if self.new_number:
                display.text = text
                self.new_number = False
            else:
                display.text += text

        elif text in '+-*/':
            if display.text:
                self.first_number = float(display.text)
                self.operation = text
                self.new_number = True

        elif text == '=':
            if self.first_number is not None and self.operation:
                second_number = float(display.text)

                if self.operation == '+':
                    result = self.first_number + second_number
                elif self.operation == '-':
                    result = self.first_number - second_number
                elif self.operation == '*':
                    result = self.first_number * second_number
                elif self.operation == '/':
                    if second_number != 0:
                        result = self.first_number / second_number
                    else:
                        result = "Error"

                expression = "{} {} {} = {}".format(
                    self.first_number, self.operation,
                    second_number, result
                )
                save_record(expression)

                display.text = str(result)
                self.first_number = None
                self.operation = None
                self.new_number = True

        elif text == 'DEL':
            if len(display.text) > 1:
                display.text = display.text[:-1]
            else:
                display.text = '0'
                self.new_number = True

        elif text == 'C':
            display.text = '0'
            self.first_number = None
            self.operation = None
            self.new_number = True


class HistoryScreen(Screen):
    history_list = ObjectProperty()

    def on_pre_enter(self, *args):
        self.refresh_history()

    def refresh_history(self):
        history_list = self.ids.history_list
        history_list.clear_widgets()
        rows = load_records()
        if not rows:
            history_list.add_widget(Label(text="История пуста"))
            return
        for _row_id, expression in rows:
            btn = Button(text=expression, size_hint_y=None, height=40)
            btn.bind(on_release=self.on_history_select)
            history_list.add_widget(btn)

    def on_history_select(self, instance):
        result = instance.text.split('=')[-1].strip()
        calc = self.manager.get_screen("Calculator")
        calc.ids.display.text = result
        calc.new_number = True

        self.manager.current = "Calculator"
        self.manager.transition.direction = "right"

    def clear_history(self):
        clear_records()
        self.refresh_history()


class WinMan(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(CalculatorRoot(name="Calculator"))
        self.add_widget(HistoryScreen(name="History"))



class CalculatorApp(App):
    def build(self):
        self.icon = 'pics/icon.png'
        init_db()
        return WinMan()



if __name__ == '__main__':
    resource_add_path(resource_path('..'))
    CalculatorApp().run()