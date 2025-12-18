from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5 import QtCore
import sys
import os
from PyQt5.QtGui import QPixmap

class Reset(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("reset-password.ui", self)

        BASE_DIR = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        ICONS_DIR = os.path.join(BASE_DIR, "Icons")

        self.reset_Button = self.findChild(QPushButton , "reset_Button")
        self.new_password_edit = self.findChild(QLineEdit, "new_password_edit")
        self.confirm_new_password_edit = self.findChild(QLineEdit, "confirm_new_password_edit")
        self.back_login_Button = self.findChild(QPushButton, "back_login_Button")

        self.email = None

        # ---- password icon 1 ----
        self.pass_label1 = self.findChild(QLabel, "pass_l1")
        lock_pixmap = QPixmap(os.path.join(ICONS_DIR, "lock_100dp_FFFFFF.png"))
        self.pass_label1.setPixmap(lock_pixmap)
        self.pass_label1.setScaledContents(True)

        # ---- password icon 2 ----
        self.pass_label2 = self.findChild(QLabel, "pass_l2")
        self.pass_label2.setPixmap(lock_pixmap)
        self.pass_label2.setScaledContents(True)

        # ---- security icon ----
        self.security_label = self.findChild(QLabel, "security_label")
        security_pixmap = QPixmap(os.path.join(ICONS_DIR, "security_100dp_FFFFFF.png"))
        self.security_label.setPixmap(security_pixmap)
        self.security_label.setScaledContents(True)