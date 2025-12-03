"""
SyAvi Time Predictor - Main Kivy App with Android Machine Locking
Works on Windows, Linux, and Android with device-locking protection
Master Key: @Hg3505050
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from datetime import datetime, timedelta
import os
import sys

# Import machine lock system
from android_machine_lock import AndroidMachineLock

# --- Helper to get relative paths ---

def resource_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

BG_IMAGE = resource_path("SyAviBackgroundPic.jpeg")
ICON_IMAGE = resource_path("SyAviTimePredictorIcon_3D.png")

# --- Lock Screen ---

class LockScreen(Screen):
    def __init__(self, lock_manager, **kwargs):
        super().__init__(**kwargs)
        self.lock_manager = lock_manager
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        with layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.bg_rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_bg, pos=self._update_bg)
        
        status = self.lock_manager.get_status()
        
        if status['locked']:
            title = Label(
                text="DEVICE LOCKED",
                font_size=24,
                bold=True,
                color=(1, 0, 0, 1),
                size_hint_y=0.3
            )
            message = Label(
                text=status['message'],
                font_size=16,
                color=(1, 1, 1, 1),
                size_hint_y=0.3
            )
            serial_label = Label(
                text=f"Serial: {status['serial']}",
                font_size=14,
                color=(0.8, 0.8, 0.8, 1),
                size_hint_y=0.2
            )
            
            layout.add_widget(title)
            layout.add_widget(message)
            layout.add_widget(serial_label)
            layout.add_widget(Label(size_hint_y=0.2))
        
        self.add_widget(layout)
    
    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

# --- Home Screen ---

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        with layout.canvas.before:
            self.bg_rect = Rectangle(source=BG_IMAGE, pos=layout.pos, size=layout.size)
        layout.bind(size=self.update_bg, pos=self.update_bg)

        top_container = BoxLayout(orientation='vertical', size_hint_y=0.5, padding=20, spacing=20)
        welcome = Label(
            text="WELCOME TO MR SY'S AVIATOR TIME PREDICTOR. LETS GO HUSTLERS",
            font_size=22,
            bold=True,
            color=(1, 1, 1, 1)
        )
        top_container.add_widget(welcome)

        start_btn = Button(
            text="START",
            size_hint=(0.5, 0.2),
            pos_hint={'center_x': 0.5},
            background_color=(0, 1, 0, 1)
        )
        start_btn.bind(on_press=self.go_to_main)
        top_container.add_widget(start_btn)

        layout.add_widget(top_container)
        layout.add_widget(Label(size_hint_y=0.5))
        self.add_widget(layout)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def go_to_main(self, instance):
        self.manager.current = "main"

# --- Main Screen ---

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.root_layout = BoxLayout(orientation='vertical')

        with self.root_layout.canvas.before:
            self.bg_rect = Rectangle(source=BG_IMAGE, pos=self.root_layout.pos, size=self.root_layout.size)
        self.root_layout.bind(size=self.update_bg, pos=self.update_bg)
        self.add_widget(self.root_layout)

        self.overlay = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.root_layout.add_widget(self.overlay)

        title = Label(
            text="TIME PREDICTIONS CALCULATION RESULTS",
            font_size=18,
            bold=True,
            size_hint_y=None,
            height=40,
            color=(1, 1, 1, 1)
        )
        self.overlay.add_widget(title)

        input_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.time_input = TextInput(
            hint_text="Time when the last Chakunata occurred (HH:MM:SS)",
            multiline=False,
            font_size=16,
            foreground_color=(0, 0, 0, 1)
        )
        self.time_input.bind(on_text_validate=self.calculate_times)
        input_layout.add_widget(self.time_input)

        calc_btn = Button(
            text="GENERATE SIGNALS",
            background_color=(0.3, 0.7, 0.3, 1)
        )
        calc_btn.bind(on_press=self.calculate_times)
        input_layout.add_widget(calc_btn)

        self.overlay.add_widget(input_layout)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.table = GridLayout(cols=5, spacing=5, size_hint_y=None)
        self.table.bind(minimum_height=self.table.setter('height'))
        self.scroll.add_widget(self.table)
        self.overlay.add_widget(self.scroll)

    def update_bg(self, *args):
        self.bg_rect.pos = self.root_layout.pos
        self.bg_rect.size = self.root_layout.size

    def calculate_times(self, instance):
        time_text = self.time_input.text.strip()
        
        if not time_text:
            return
        
        try:
            parts = time_text.split(':')
            if len(parts) != 3:
                raise ValueError("Invalid format")
            
            hours, minutes, seconds = map(int, parts)
            input_time = datetime.strptime(f"{hours:02d}:{minutes:02d}:{seconds:02d}", "%H:%M:%S").time()
            base_time = datetime.combine(datetime.today(), input_time)
            
            self.table.clear_widgets()
            
            headers = ["Time", "Minutes", "Seconds", "Probability", "Status"]
            for header in headers:
                self.table.add_widget(Label(
                    text=header,
                    bold=True,
                    size_hint_y=None,
                    height=40,
                    color=(1, 1, 1, 1)
                ))
            
            for i in range(1, 11):
                new_time = base_time + timedelta(minutes=i*3)
                time_str = new_time.strftime("%H:%M:%S")
                
                prob = 85 + (i % 5) * 2
                status = "WIN" if prob > 88 else "RISKY"
                status_color = (0, 1, 0, 1) if status == "WIN" else (1, 1, 0, 1)
                
                self.table.add_widget(Label(
                    text=time_str,
                    size_hint_y=None,
                    height=40,
                    color=(1, 1, 1, 1)
                ))
                self.table.add_widget(Label(
                    text=str(i*3),
                    size_hint_y=None,
                    height=40,
                    color=(1, 1, 1, 1)
                ))
                self.table.add_widget(Label(
                    text="0",
                    size_hint_y=None,
                    height=40,
                    color=(1, 1, 1, 1)
                ))
                self.table.add_widget(Label(
                    text=f"{prob}%",
                    size_hint_y=None,
                    height=40,
                    color=(1, 1, 1, 1)
                ))
                self.table.add_widget(Label(
                    text=status,
                    size_hint_y=None,
                    height=40,
                    color=status_color
                ))
        
        except:
            pass

# --- Main App ---

class SyAviTimePredictorApp(App):
    def build(self):
        # Initialize machine lock
        self.lock_manager = AndroidMachineLock()
        status = self.lock_manager.get_status()
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add lock screen if device is locked to a different serial
        if status['locked']:
            # Device already locked - show lock screen
            sm.add_widget(LockScreen(self.lock_manager, name='lock'))
            sm.current = 'lock'
        else:
            # Device not locked - proceed normally
            sm.add_widget(HomeScreen(name='home'))
            sm.add_widget(MainScreen(name='main'))
            sm.current = 'home'
        
        return sm

if __name__ == '__main__':
    app = SyAviTimePredictorApp()
    app.title = 'SyAvi Time Predictor'
    app.icon = ICON_IMAGE
    app.run()