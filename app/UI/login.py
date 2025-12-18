from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5 import QtCore
import sys
import os
from PyQt5.QtGui import QIcon , QPixmap


class Login(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("Login.ui", self)

        BASE_DIR = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        ICONS_DIR = os.path.join(BASE_DIR, "icons")

        self.email_edit = self.findChild(QLineEdit , "email_edit")
        self.password_edit = self.findChild(QLineEdit , "password_edit")
        self.login_button = self.findChild(QPushButton, "login_Button")
        self.forget_button = self.findChild(QPushButton, "forget_Button")

        self.return_home_button = self.findChild(QPushButton, "return_home")
        self.return_home_button.setIcon(QIcon(os.path.join(ICONS_DIR, "home_100dp_FFFFFF.png")))

        self.email_label = self.findChild(QLabel, "email_label")
        email_pixmap = QPixmap(os.path.join(ICONS_DIR, "email_100dp_FFFFFF.png"))
        self.email_label.setPixmap(email_pixmap)
        self.email_label.setScaledContents(True)

        self.password_label = self.findChild(QLabel, "pass_label")
        pass_pixmap = QPixmap(os.path.join(ICONS_DIR, "lock_100dp_FFFFFF.png"))
        self.password_label.setPixmap(pass_pixmap)
        self.password_label.setScaledContents(True)
