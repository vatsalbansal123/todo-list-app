# Imports
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import IRightBodyTouch, ILeftBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.list import IconLeftWidget, IconRightWidget
from kivymd.uix.boxlayout import MDBoxLayout
import sqlite3, json


# Window Dimensions
window_width, window_height = 400, 600

# Apply to the window
def set_window():
    Config.set("graphics", "resizable", False)
    Config.set("graphics", "width", window_width)
    Config.set("graphics", "height", window_height)
    Config.write()
