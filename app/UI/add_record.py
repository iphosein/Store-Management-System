from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5 import QtCore
import sys

class Addrecord(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("add-record.ui", self)


        self.create_button = self.findChild(QPushButton, "create_button")
        self.cancel_button = self.findChild(QPushButton, "cancel_button")

        self.scroll_area = self.findChild(QScrollArea, "scrollArea")



