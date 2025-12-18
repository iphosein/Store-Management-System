from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5 import QtCore
import sys
import os
from PyQt5.QtGui import QPixmap

class Forget(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("forget-password.ui", self)

        self.back_to_login_button = self.findChild(QPushButton, "back_login_Button")
        self.send_email_button = self.findChild(QPushButton, "send_email_Button")
        self.email_edit = self.findChild(QLineEdit , "email_edit")
        BASE_DIR = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        ICONS_DIR = os.path.join(BASE_DIR, "Icons")
        # ---- email icon ----
        self.email_label = self.findChild(QLabel, "email_label")
        email_pixmap = QPixmap(os.path.join(ICONS_DIR, "email_100dp_FFFFFF.png"))
        self.email_label.setPixmap(email_pixmap)
        self.email_label.setScaledContents(True)

        # ---- info icon ----
        self.info_label = self.findChild(QLabel, "info_label")
        info_pixmap = QPixmap(os.path.join(ICONS_DIR, "info_outline_100dp_FFFFFF.png"))
        self.info_label.setPixmap(info_pixmap)
        self.info_label.setScaledContents(True)