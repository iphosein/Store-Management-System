from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5 import QtCore
import sys
import os
from PyQt5.QtGui import QIcon

class Reports(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("reports.ui", self)

        BASE_DIR = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        ICONS_DIR = os.path.join(BASE_DIR, "Icons")

        self.filter_result_Button = self.findChild(QPushButton, "filter_result_Button")


        self.scroll_area = self.findChild(QScrollArea, "scrollArea")


        self.return_home_button = self.findChild(QPushButton, "return_home")
        self.return_home_button.setIcon(QIcon(os.path.join(ICONS_DIR, "home_100dp_FFFFFF.png")))


        self.to_time = self.findChild(QDateTimeEdit, "from_time")
        self.to_time.setCalendarPopup(True)
        self.from_time = self.findChild(QDateTimeEdit, "to_time")
        self.from_time.setCalendarPopup(True)