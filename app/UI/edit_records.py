from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5 import QtCore
import sys

class Editrecord(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("edit-record.ui", self)


        self.apply_changes_button = self.findChild(QPushButton, "apply_changes_button")
        self.cancel_button = self.findChild(QPushButton, "cancel_button")

        self.scroll_area = self.findChild(QScrollArea, "scrollArea")



