from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from datetime import datetime, timedelta
import os
import sys

# --- Helper to get relative paths (works on PC and Android) ---

def resource_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS # Indentation fixed here
    else:                      # Indentation fixed here
        base_path = os.path.dirname(os.path.abspath(__file__)) # Indentation fixed, `**file**` -> `__file__`
    return os.path.join(base_path, filename)

# Paths

BG_IMAGE = resource_path("SyAviBackgroundPic.jpeg")
ICON_IMAGE = resource_path("SyAviTimePredictorIcon_3D.png")

# --- Home Screen ---

class HomeScreen(Screen):
    def __init__(self, **kwargs): # `**init**` -> `__init__`
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Background image
        with layout.canvas.before:
            self.bg_rect = Rectangle(source=BG_IMAGE, pos=layout.pos, size=layout.size)
        layout.bind(size=self.update_bg, pos=self.update_bg)

        # Top container
        top_container = BoxLayout(orientation='vertical', size_hint_y=0.5, padding=20, spacing=20)
        welcome = Label(
            text="WELCOME TO MR SY'S AVIATOR TIME PREDICTOR. LETS GO HUSTLERS",
            font_size=22,
            bold=True,
            color=(1,1,1,1)
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
        layout.add_widget(Label(size_hint_y=0.5))  # spacer
        self.add_widget(layout)

    def update_bg(self, *args): # Indentation fixed (inside the class)
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def go_to_main(self, instance): # Indentation fixed (inside the class)
        self.manager.current = "main"

# --- Main Screen ---

class MainScreen(Screen):
    def __init__(self, **kwargs): # `**init**` -> `__init__`
        super().__init__(**kwargs)

        self.root_layout = BoxLayout(orientation='vertical')

        # Background
        with self.root_layout.canvas.before:
            self.bg_rect = Rectangle(source=BG_IMAGE, pos=self.root_layout.pos, size=self.root_layout.size)
        self.root_layout.bind(size=self.update_bg, pos=self.update_bg)
        self.add_widget(self.root_layout)

        # Overlay layout
        self.overlay = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.root_layout.add_widget(self.overlay)

        title = Label(
            text="TIME PREDICTIONS CALCULATION RESULTS",
            font_size=18,
            bold=True,
            size_hint_y=None,
            height=40,
            color=(1,1,1,1)
        )
        self.overlay.add_widget(title)

        input_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.time_input = TextInput(
            hint_text="Time when the last Chakunata occurred (HH:MM:SS)",
            multiline=False,
            font_size=16,
            foreground_color=(0,0,0,1)
        )
        self.time_input.bind(on_text_validate=self.calculate_times)
        input_layout.add_widget(self.time_input)

        calc_btn = Button(
            text="GENERATE SIGNALS",
            background_color=(0.3,0.7,0.3,1)
        )
        calc_btn.bind(on_press=self.calculate_times)
        input_layout.add_widget(calc_btn)

        self.overlay.add_widget(input_layout)

        self.scroll = ScrollView(size_hint=(1,1))
        self.table = GridLayout(cols=5, spacing=5, size_hint_y=None)
        self.table.bind(minimum_height=self.table.setter('height'))
        self.scroll.add_widget(self.table)
        self.overlay.add_widget(self.scroll)

    def update_bg(self, *args): # Indentation fixed
        self.bg_rect.pos = self.root_layout.pos
        self.bg_rect.size = self.root_layout.size

    # --- Helper to swap digits ---
    def swap_digits(self, value): # Indentation fixed
        s = f"{value:02}"
        return int(s[1] + s[0])

    # --- Helper to normalize time ---
    def normalize_time(self, h, m, s): # Indentation fixed
        if s >= 60:
            m += s // 60
            s = s % 60
        if m >= 60:
            h += m // 60
            m = m % 60
        h = h % 24
        return h, m, s

    def calculate_times(self, instance): # Indentation fixed
        self.table.clear_widgets()
        time_input = self.time_input.text
        try:
            base_time = datetime.strptime(time_input, "%H:%M:%S")
        except ValueError:
            self.table.add_widget(Label(text="Invalid time format! Use HH:MM:SS", color=(1,0,0,1)))
            return

        # --- Step 1: Next 10 times (+4m+4s) ---
        increment_1 = timedelta(minutes=4, seconds=4)
        current_time = base_time
        next_10_times = []
        for _ in range(10):
            current_time += increment_1
            next_10_times.append(current_time.strftime("%H:%M:%S"))

        # --- Step 2: Custom add minutes and seconds, normalized ---
        step2_min = base_time.minute + base_time.minute
        step2_sec = base_time.second + base_time.second
        h2, m2, s2 = self.normalize_time(base_time.hour, step2_min, step2_sec)
        step2_time = base_time.replace(hour=h2, minute=m2, second=s2)

        # --- Step 3: +10m +10s ---
        step3_time = base_time + timedelta(minutes=10, seconds=10)
        h3, m3, s3 = self.normalize_time(step3_time.hour, step3_time.minute, step3_time.second)
        step3_time = step3_time.replace(hour=h3, minute=m3, second=s3)

        # --- Step 4: +20m +20s from base time, then extra increments for rows 2-4 ---
        base_step4_time = base_time + timedelta(minutes=20, seconds=20)
        h4, m4, s4 = self.normalize_time(base_step4_time.hour, base_step4_time.minute, base_step4_time.second)
        step4_row1 = base_step4_time.replace(hour=h4, minute=m4, second=s4)

        # Rows 2-4 with extra 1,2,3 minutes
        step4_row2_h, step4_row2_m, step4_row2_s = self.normalize_time(h4, m4 + 1, s4)
        step4_row3_h, step4_row3_m, step4_row3_s = self.normalize_time(step4_row2_h, step4_row2_m + 2, step4_row2_s)
        step4_row4_h, step4_row4_m, step4_row4_s = self.normalize_time(step4_row3_h, step4_row3_m + 3, step4_row3_s)

        step4_times = [
            step4_row1.strftime("%H:%M:%S"), # Formatted correctly
            f"{step4_row2_h:02}:{step4_row2_m:02}:{step4_row2_s:02}", # Formatted correctly
            f"{step4_row3_h:02}:{step4_row3_m:02}:{step4_row3_s:02}", # Formatted correctly
            f"{step4_row4_h:02}:{step4_row4_m:02}:{step4_row4_s:02}"  # Formatted correctly
        ]

        # --- Step 5: TimeSwitch ---
        swapped_min = self.swap_digits(base_time.minute)
        swapped_sec = self.swap_digits(base_time.second)
        h5, m5, s5 = self.normalize_time(base_time.hour, swapped_min, swapped_sec)
        step5_time = base_time.replace(hour=h5, minute=m5, second=s5)

        # --- Table headers ---
        headers = ["No.", "2X or More", "5X or More sig1", "+10 SIG2 5X >=", "+20 SIG2 5X >="]
        for idx, h_text in enumerate(headers):
            size_x = 0.5 if idx==0 else 1
            self.table.add_widget(Label(text=h_text, bold=True, size_hint_y=None, height=40, size_hint_x=size_x, font_size=16, color=(1,1,1,1)))

# Assuming this code is within a class method, e.g., def setup_table(self):

        for i in range(10):
            # Column 1: No.
            self.table.add_widget(Label(text=str(i+1), size_hint_y=None, height=40, size_hint_x=0.5, color=(1,1,1,1)))

            # Column 2: Step1 purple
            label_step1 = Label(
                text=next_10_times[i],
                size_hint_y=None,
                height=40,
                color=(1,1,1,1),
                bold=True,
                size_hint_x=1
            )
            with label_step1.canvas.before:
                Color(0.6,0.3,0.7,1)
                rect1 = Rectangle(pos=label_step1.pos, size=label_step1.size)
            label_step1.bind(pos=lambda inst,val,r=rect1: setattr(r,'pos',inst.pos))
            label_step1.bind(size=lambda inst,val,r=rect1: setattr(r,'size',inst.size))
            self.table.add_widget(label_step1)

            # Column 3: Step2 (sig1) and Step5 TimeSwitch
            if i == 0:
                # Step2 result
                label_sig1 = Label(
                    text=step2_time.strftime("%H:%M:%S"),
                    size_hint_y=None,
                    height=40,
                    color=(1,1,1,1),
                    bold=True
                )
                with label_sig1.canvas.before:
                    Color(1,0.4,0.8,1)  # pink
                    rect_sig1 = Rectangle(pos=label_sig1.pos, size=label_sig1.size)
                label_sig1.bind(pos=lambda inst,val,r=rect_sig1: setattr(r,'pos',inst.pos))
                label_sig1.bind(size=lambda inst,val,r=rect_sig1: setattr(r,'size',inst.size))
                self.table.add_widget(label_sig1)
            elif i == 2:
                self.table.add_widget(Label(text="TymSwitch", size_hint_y=None, height=40, color=(1,1,1,1), bold=True))
            elif i == 3:
                label_sw = Label(
                    text=step5_time.strftime("%H:%M:%S"),
                    size_hint_y=None,
                    height=40,
                    color=(1,1,1,1),
                    bold=True
                )
                with label_sw.canvas.before:
                    Color(1,0.4,0.8,1)
                    rect_sw = Rectangle(pos=label_sw.pos, size=label_sw.size)
                label_sw.bind(pos=lambda inst,val,r=rect_sw: setattr(r,'pos',inst.pos))
                label_sw.bind(size=lambda inst,val,r=rect_sw: setattr(r,'size',inst.size))
                self.table.add_widget(label_sw)
            else:
                self.table.add_widget(Label(text="", size_hint_y=None, height=40))

            # Column 4: Step3
            if i == 0:
                label_step3 = Label(
                    text=step3_time.strftime("%H:%M:%S"),
                    size_hint_y=None,
                    height=40,
                    color=(1,1,1,1),
                    bold=True
                )
                with label_step3.canvas.before:
                    Color(1,0.4,0.8,1)
                    rect_s3 = Rectangle(pos=label_step3.pos, size=label_step3.size)
                label_step3.bind(pos=lambda inst,val,r=rect_s3: setattr(r,'pos',inst.pos))
                label_step3.bind(size=lambda inst,val,r=rect_s3: setattr(r,'size',inst.size))
                self.table.add_widget(label_step3)
            else:
                self.table.add_widget(Label(text="", size_hint_y=None, height=40))

            # Column 5: Step4 rows with purple background
            if i in [0,1,2,3]:
                if i == 0:
                    h_, m_, s_ = h4, m4, s4
                elif i == 1:
                    h_, m_, s_ = step4_row2_h, step4_row2_m, step4_row2_s
                elif i == 2:
                    h_, m_, s_ = step4_row3_h, step4_row3_m, step4_row3_s
                elif i == 3:
                    h_, m_, s_ = step4_row4_h, step4_row4_m, step4_row4_s
                label_step4 = Label(
                    text=f"{h_:02}:{m_:02}:{s_:02}",
                    size_hint_y=None,
                    height=40,
                    color=(1,1,1,1),
                    bold=True
                )
                with label_step4.canvas.before:
                    Color(0.6,0.3,0.7,1)
                    rect_s4 = Rectangle(pos=label_step4.pos, size=label_step4.size)
                label_step4.bind(pos=lambda inst,val,r=rect_s4: setattr(r,'pos',inst.pos))
                label_step4.bind(size=lambda inst,val,r=rect_s4: setattr(r,'size',inst.size))
                self.table.add_widget(label_step4)
            else:
                self.table.add_widget(Label(text="", size_hint_y=None, height=40))

# --- App ---
# This part requires proper class and function headers

class TimeCalculatorApp(App):
    def build(self):
        self.icon = ICON_IMAGE
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(MainScreen(name="main"))
        return sm

if __name__ == "__main__":
    TimeCalculatorApp().run()
