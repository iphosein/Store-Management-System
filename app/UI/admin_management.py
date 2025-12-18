from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5 import QtCore
import sys
import os
from PyQt5.QtGui import QIcon

class Admin(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("admin-management.ui", self)

        BASE_DIR = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        ICONS_DIR = os.path.join(BASE_DIR, "Icons")

        self.field_combo_box = self.findChild(QComboBox, "field_combo")
        self.filter_result_Button = self.findChild(QPushButton, "filter_result_Button")
        self.value_edit = self.findChild(QLineEdit, "value_Edit")
        self.back_page_button = self.findChild(QPushButton, "back_page_Button")
        self.back_page_button.setIcon(QIcon(os.path.join(ICONS_DIR, "arrow_circle_left_100dp_999999.png")))

        self.next_page_button = self.findChild(QPushButton, "next_page_Button")
        self.next_page_button.setIcon(QIcon(os.path.join(ICONS_DIR, "arrow_circle_right_100dp_FFFFFF.png")))

        self.scroll_area = self.findChild(QScrollArea, "scrollArea")

        self.edit_button = self.findChild(QPushButton, "edit_Button")
        self.edit_button.setIcon(QIcon(os.path.join(ICONS_DIR, "edit_100dp_FFFFFF.png")))

        self.delete_button = self.findChild(QPushButton, "delete_Button")
        self.delete_button.setIcon(QIcon(os.path.join(ICONS_DIR, "delete_forever_100dp_FFFFFF.png")))

        self.add_button = self.findChild(QPushButton, "add_Button")
        self.add_button.setIcon(QIcon(os.path.join(ICONS_DIR, "add_circle_outline_100dp_FFFFFF.png")))

        self.return_home_button = self.findChild(QPushButton, "return_home")
        self.return_home_button.setIcon(QIcon(os.path.join(ICONS_DIR, "home_100dp_FFFFFF.png")))





