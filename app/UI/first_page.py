from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5 import QtCore
import sys

class First(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("first-page.ui", self)

