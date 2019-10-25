"""
A .py file to generate kivy user interface to facilitate
easy primer generation and order placement template for IDT. 
"""
import os
import datetime
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color
kivy.require("1.10.1")
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'borderless', 0)
MAIN_DIR = os.path.dirname(os.path.abspath(__file__))


class FontSize:
    """
    Set fontsize for Kivy GUI interface.
    """
    def __init__(self):
        self.header_size = 36
        self.subheader_size = 21
        self.label_size = 17
        self.bttn_size = 25


class ColorFormat:
    """
    Set color for Kivy GUI font and background
    """
    def __init__(self):
        self.bttn_bckgrd_color = (0.00, 0.29, 0.52, 1.00)
        self.scrn_bckgrd_color = (1.00, 1.00, 1.00, 1.00)
        self.bttn_bck_color = (1.00, 0.41, 0.14, 1.00)
        self.bttn_fwd_color = (0.22, 0.66, 0.76, 1.00)
        self.header_color = (0.00, 0.29, 0.52, 1.00)


class WorklistGenerator(GridLayout):
    """
    Define layout for Kivy GUI with button properties
    """
    def __init__(self, **kwargs):
        super(WorklistGenerator, self).__init__(**kwargs)
        self.fontsize = FontSize()
        self.colorformat = ColorFormat()

        with self.canvas:
            Color(rgba=self.colorformat.scrn_bckgrd_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect,
                  size=self.update_rect)

        self.inside = GridLayout()
        self.inside.cols = 3

        self.inside1 = GridLayout()
        self.inside1.cols = 1

        self.inside2 = GridLayout()
        self.inside2.cols = 1

        self.inside3 = GridLayout()
        self.inside3.cols = 1

        self.inside4 = GridLayout()
        self.inside4.cols = 1

        self.cols = 1

        self.inside1.add_widget(Label(text=""))
        self.inside2.add_widget(Label(text=""))
        self.inside3.add_widget(Label(text=""))
        self.inside4.add_widget(Label(text=""))

        self.close_select = Button(text="[b]CLOSE[/b]", markup=True,
                                   color=self.colorformat.bttn_bck_color,
                                   background_normal='',
                                   background_color=self.colorformat.bttn_bckgrd_color,
                                   font_size=self.fontsize.bttn_size)
        self.close_select.bind(on_press=self.close)
        self.inside.add_widget(self.close_select)

        self.tube_select = Button(text="[b]SINGLE TUBES[/b]", markup=True,
                                  color=self.colorformat.bttn_fwd_color,
                                  background_normal='',
                                  background_color=self.colorformat.bttn_bckgrd_color,
                                  font_size=self.fontsize.bttn_size)
        self.tube_select.bind(on_press=self.tube)
        self.inside.add_widget(self.tube_select)

        self.plate_select = Button(text="[b]96-WELL PLATE[/b]", markup=True,
                                   color=self.colorformat.bttn_fwd_color,
                                   background_normal='',
                                   background_color=self.colorformat.bttn_bckgrd_color,
                                   font_size=self.fontsize.bttn_size)
        self.plate_select.bind(on_press=self.plate)
        self.inside.add_widget(self.plate_select)

        self.status = Label(text=f'[b][u]Status[/u]:    Incomplete\n[u]Results Folder[/u]:    N/A[/b]',
                            markup=True, color=self.colorformat.header_color,
                            font_size=self.fontsize.subheader_size)

        self.add_widget(self.inside1)
        self.add_widget(self.inside2)
        self.add_widget(Label(text="[b][i]Bulk Primer Walk for IDT[/i][/b]", markup=True,
                              color=self.colorformat.header_color,
                              font_size=self.fontsize.header_size))
        self.add_widget(self.status)
        self.add_widget(self.inside3)
        self.add_widget(self.inside4)
        self.add_widget(self.inside)

    def close(self, instance):
        """Button func. for exiting application"""
        if instance:
            App.get_running_app().stop()
            reset()

    def tube(self, instance):
        """Button func. to select tube format"""
        if instance:
            global order_type
            order_type = 'tube'
            exec(open("Primerwalk.py").read(), globals(), globals())
            os.chdir(MAIN_DIR)
            self.status.text = f'[b][u]Status[/u]:    Single Tubes Complete\n[u]Results Folder[/u]:    "{datetime.date.today()}"[/b]'

    def plate(self, instance):
        """Button func. to select plate format"""
        if instance:
            global order_type
            order_type = 'plate'
            exec(open("Primerwalk.py").read(), globals(), globals())
            os.chdir(MAIN_DIR)
            self.status.text = f'[b][u]Status[/u]:    96-Well Plate Complete\n[u]Results Folder[/u]:    "{datetime.date.today()}"[/b]'

    def update_rect(self, *args):
        """Set button size"""
        self.rect.pos = self.pos
        self.rect.size = self.size


def reset():
    """Reset Kivy application upon button click to avoid stack overflow"""
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}


class WorklistGeneratorApp(App):
    """
    Build application
    """
    def build(self):
        return WorklistGenerator()


if __name__ == "__main__":
    WorklistGeneratorApp().run()
    reset()
