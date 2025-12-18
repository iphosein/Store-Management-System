from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QSize , QDateTime, QDate, QTime , Qt
from PyQt5.QtGui import QPixmap, QIcon
import sys
import httpx
import os


from login import Login
from admin_management import Admin
from forget_password import Forget
from reset_password import Reset
from first_page import First
from customers import Customers
from invoices import Invoices
from product import Product
from add_record import Addrecord
from edit_records import Editrecord
from reports_page import Reports


sys.path.append("L:/Hosein/mentorschip/store-management")
from app import models

class AddCard(QWidget):
    def __init__(self, columns):
        super().__init__()

        self.inputs = {}  # to store QLineEdit fields

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # We skip ID (auto increment)
        for col in columns:
            if col == "id":
                continue

            row_box = QHBoxLayout()

            label = QLabel(col.capitalize() + ":")
            edit = QLineEdit()

            row_box.addWidget(label)
            row_box.addWidget(edit)

            layout.addLayout(row_box)

            self.inputs[col] = edit  # store for later access

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background: #ffffff;
                border-radius: 10px;
                border: 1px solid #c9c9c9;
            }
            QWidget:hover {
                border: 2px solid #006eff;
            }
            QLabel { font-size: 13px; }
            QLineEdit {
                padding: 5px;
                border: 1px solid #bcbcbc;
                border-radius: 6px;
            }
        """)


class RecordCard(QWidget):
    def __init__(self, record_data: dict):
        super().__init__()

        self.record_data = record_data
        self.pk = record_data.get("id", None)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)

        self.select_radio = QRadioButton()
        main_layout.addWidget(self.select_radio)

        info_container = QWidget()
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        info_layout.setContentsMargins(0, 0, 0, 0)

        for key, value in self.record_data.items():
            info_layout.addWidget(QLabel(f"{key}: {value}"))

        info_container.setLayout(info_layout)
        main_layout.addWidget(info_container)

        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget {
                background: #ffffff;
                border-radius: 10px;
                border: 1px solid #c9c9c9;
            }
            QWidget:hover {
                border: 2px solid #006eff;
            }
            QLabel {
                font-size: 12px;
            }
        """)


class EditCard(QWidget):
    def __init__(self, record_data: dict):
        super().__init__()

        self.record_data = record_data
        self.inputs = {}  # To store editable QLineEdit fields

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # ---- Show ID but disable editing ----
        if "id" in record_data:
            id_row = QHBoxLayout()
            id_label = QLabel("ID:")
            id_edit = QLineEdit(str(record_data["id"]))
            id_edit.setDisabled(True)

            id_row.addWidget(id_label)
            id_row.addWidget(id_edit)

            layout.addLayout(id_row)

            self.inputs["id"] = id_edit  # keep but read-only

        # ---- Generate editable fields ----
        for key, value in record_data.items():
            if key == "id":
                continue

            row_box = QHBoxLayout()

            label = QLabel(key.capitalize() + ":")
            edit = QLineEdit(str(value))

            row_box.addWidget(label)
            row_box.addWidget(edit)

            layout.addLayout(row_box)

            self.inputs[key] = edit

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background: #ffffff;
                border-radius: 10px;
                border: 1px solid #c9c9c9;
            }
            QWidget:hover {
                border: 2px solid #006eff;
            }
            QLabel { font-size: 13px; }
            QLineEdit {
                padding: 5px;
                border: 1px solid #bcbcbc;
                border-radius: 6px;
            }
        """)


    def get_updated_values(self):
        """Convert QLineEdits back to dict for PUT request."""
        result = {}
        for key, widget in self.inputs.items():
            result[key] = widget.text().strip()
        return result


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Home-Page.ui", self)

        self.setWindowTitle("Store Management")

        #Api Url define
        self.url = "http://127.0.0.1:8000"
        self.jwt = None

        # self.menubar = self.findChild(QMenuBar , "menubar")
        self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")
        self.login_button = self.findChild(QPushButton, "login_Button")
        self.hello_label = self.findChild(QLabel, "hello_label")
        self.admin_management_button = self.findChild(QPushButton, "admin_management_Button")
        self.customers_button =self.findChild(QPushButton, "customers_Button")
        self.products_button =self.findChild(QPushButton, "products_Button")
        self.invoices_button = self.findChild(QPushButton, "invoices_Button")
        self.reports_button = self.findChild(QPushButton, "reports_Button")
        self.statusBar = self.findChild(QStatusBar, "statusbar")


        #set enable buttons = False exception Login
        self.buttons = [self.reports_button , self.admin_management_button ,
                        self.customers_button , self.products_button , self.invoices_button]
        for button in self.buttons:
            button.setEnabled(False)

        #text for before login
        self.hello_label.setText("Welcome! Please Log In")


        #all pages variables
        self.page_first = First()
        self.page_login = Login()
        self.page_forget = Forget()
        self.page_admin = Admin()
        self.page_reset = Reset()
        self.page_customers = Customers()
        self.page_products = Product()
        self.page_invoices = Invoices()
        self.page_add_records = Addrecord()
        self.page_edit_records = Editrecord()
        self.page_reports = Reports()

        #add all pages to stackedWidget
        self.stackedWidget.addWidget(self.page_first)
        self.stackedWidget.addWidget(self.page_login)
        self.stackedWidget.addWidget(self.page_forget)
        self.stackedWidget.addWidget(self.page_admin)
        self.stackedWidget.addWidget(self.page_reset)
        self.stackedWidget.addWidget(self.page_customers)
        self.stackedWidget.addWidget(self.page_products)
        self.stackedWidget.addWidget(self.page_invoices)
        self.stackedWidget.addWidget(self.page_add_records)
        self.stackedWidget.addWidget(self.page_edit_records)
        self.stackedWidget.addWidget(self.page_reports)

        # first page ui
        self.stackedWidget.setCurrentWidget(self.page_first)


        self.login_button.clicked.connect(self.open_login_logout)
        self.admin_management_button.clicked.connect(self.open_admin_management)



        self.page_login.return_home_button.clicked.connect(self.return_home)

        self.page_forget.back_to_login_button.clicked.connect(self.return_home)

        self.page_forget.back_to_login_button.clicked.connect(self.open_login_logout)
        self.page_login.forget_button.clicked.connect(self.open_forget_page)
        self.page_login.login_button.clicked.connect(self.login_auth)

        self.page_reset.back_login_Button.clicked.connect(self.open_login_logout)
        self.page_reset.reset_Button.clicked.connect(self.reset_password)

        self.page_forget.send_email_button.clicked.connect(self.open_reset_page)

        self.customers_button.clicked.connect(self.open_customers_page)
        self.page_customers.return_home_button.clicked.connect(self.return_home)
        self.page_customers.edit_button.clicked.connect(lambda : self.open_edit_records_page("Customer"))
        # self.page_customers.add_button.clicked.connect(lambda : self.open_add_records_page("Customer"))

        self.page_customers.add_button.clicked.connect(self.open_add_records_page)

        self.page_customers.filter_result_Button.clicked.connect(self.filtered_result)
        self.page_customers.delete_button.clicked.connect(self.delete_record)



        self.products_button.clicked.connect(self.open_products_page)
        self.page_products.return_home_button.clicked.connect(self.return_home)
        self.page_products.edit_button.clicked.connect(lambda : self.open_edit_records_page("Product"))

        self.page_products.add_button.clicked.connect(self.open_add_records_page)

        self.page_products.filter_result_Button.clicked.connect(self.filtered_result)
        self.page_products.delete_button.clicked.connect(self.delete_record)



        self.invoices_button.clicked.connect(self.open_invoices_page)
        self.page_invoices.return_home_button.clicked.connect(self.return_home)
        self.page_invoices.edit_button.clicked.connect(lambda : self.open_edit_records_page("Invoice"))

        self.page_invoices.add_button.clicked.connect(self.open_add_records_page)

        self.page_invoices.filter_result_Button.clicked.connect(self.filtered_result)
        self.page_invoices.delete_button.clicked.connect(self.delete_record)


        #Add record page
        self.previous_page_callback = None

        self.page_add_records.cancel_button.clicked.connect(lambda : self.previous_page_callback())
        self.page_edit_records.cancel_button.clicked.connect(lambda : self.previous_page_callback())

        self.page_add_records.create_button.clicked.connect(self.submit_add_records)
        self.page_edit_records.apply_changes_button.clicked.connect(self.submit_edit_records_page)

        #admin management page
        self.page_admin.return_home_button.clicked.connect(self.return_home)

        self.page_admin.add_button.clicked.connect(self.open_add_records_page)

        self.page_admin.edit_button.clicked.connect(lambda :self.open_edit_records_page("Admin"))
        self.page_admin.filter_result_Button.clicked.connect(self.filtered_result)
        self.page_admin.delete_button.clicked.connect(self.delete_record)

        self.radio_group = QButtonGroup()
        self.radio_group.setExclusive(True)

        self.admin_cards = []
        self.customer_cards = []
        self.product_cards = []
        self.invoice_cards = []

        self.limit = 2
        self.skip = 0

        self.page_admin.next_page_button.clicked.connect(lambda : self.next_previous("n",self.page_admin))
        self.page_admin.back_page_button.clicked.connect(lambda : self.next_previous("b",self.page_admin))

        self.page_products.next_page_button.clicked.connect(lambda : self.next_previous("n",self.page_products))
        self.page_products.back_page_button.clicked.connect(lambda : self.next_previous("b",self.page_products))

        self.page_customers.next_page_button.clicked.connect(lambda : self.next_previous("n",self.page_customers))
        self.page_customers.back_page_button.clicked.connect(lambda : self.next_previous("b",self.page_customers))

        self.page_invoices.next_page_button.clicked.connect(lambda : self.next_previous("n",self.page_invoices))
        self.page_invoices.back_page_button.clicked.connect(lambda : self.next_previous("b",self.page_invoices))

        self.reports_button.clicked.connect(self.open_reports_page)
        self.page_reports.return_home_button.clicked.connect(self.return_home)
        self.page_reports.filter_result_Button.clicked.connect(self.show_reports)


    def return_home(self):
        self.stackedWidget.setCurrentWidget(self.page_first)


    def open_login_logout(self):
        if not self.jwt :
            self.stackedWidget.setCurrentWidget(self.page_login)
            self.page_login.email_edit.setText("")
            self.page_login.email_edit.setPlaceholderText("Email Address")

            self.page_login.password_edit.setText("")
            self.page_login.password_edit.setPlaceholderText("Password")

        else :
            self.stackedWidget.setCurrentWidget(self.page_first)
            self.jwt = None
            self.statusBar.showMessage("You have successfully logged out.")
            for button in self.buttons :
                button.setEnabled(False)
            QMessageBox.information(None,"Goodbye!","You have successfully logged out.")
            self.hello_label.setText("Welcome! Please Log In")


    def login_auth(self):
        if self.page_login.email_edit.text().strip() and self.page_login.password_edit.text().strip() :
            payload = {"email": self.page_login.email_edit.text()  , "password": self.page_login.password_edit.text() }

            try :
                response = httpx.post(f"{self.url}/login", json=payload)
                if response.status_code == 403 :
                    QMessageBox.warning(None,"Error", "Incorrect username or password!")
                else :
                    data = response.json()

                    self.hello_label.setText(f"Hello {data.get('name')}, welcome to the panel!")

                    self.stackedWidget.setCurrentWidget(self.page_first)
                    for button in self.buttons :
                        button.setEnabled(True)
                    QMessageBox.information(None,"Hey there !", "You have successfully logged in")
                    self.statusBar.showMessage("You have successfully logged in")

                    self.jwt = data.get("access_token")


            except Exception as e:
                QMessageBox.critical(None, "Error", f"Connect to DataBase field")
                self.statusbar.showMessage(f"{e}")

        else :
            QMessageBox.warning(None,"Error", "Please complete your login credentials!")


    def open_forget_page(self):
        self.stackedWidget.setCurrentWidget(self.page_forget)
        self.page_forget.email_edit.setText("")
        self.page_forget.email_edit.setPlaceholderText("Enter your Email Address")


    def open_reset_page(self):
        email = self.page_forget.email_edit.text().strip().lower()

        if not email:
            QMessageBox.warning(None, "Error", "Please enter your Email Address!")
            return

        payload = {"email": email }
        try :
            response = httpx.post(f"{self.url}/login/forget", json=payload)

            if response.status_code == 404:
                QMessageBox.warning(None, "Error", "This email is not associated with any account")
                return

            if response.status_code != 200:
                QMessageBox.warning(None, "Error", "Something went wrong")
                return

            data = response.json()

            if data.get("message") == "OK":
                self.stackedWidget.setCurrentWidget(self.page_reset)
                self.page_reset.email = email
                self.page_reset.new_password_edit.setText("")
                self.page_reset.new_password_edit.setPlaceholderText("Enter New Password")
                self.page_reset.confirm_new_password_edit.setText("")
                self.page_reset.confirm_new_password_edit.setPlaceholderText("Confirm New Password")

            else:
                QMessageBox.warning(None, "Error", "Unexpected response")
                return


        except Exception as e:
            QMessageBox.critical(None, "Error", f"Connection Failed: {e}")


    def reset_password(self):
        new = self.page_reset.new_password_edit.text().strip()
        confirm = self.page_reset.confirm_new_password_edit.text().strip()

        if not new or not confirm :
            QMessageBox.warning(None, "Error", "Please enter new password")
            return

        elif new != confirm :
            QMessageBox.warning(None,"Error", "Passwords do not match.")
            return

        try:
            payload = {"email": self.page_reset.email , "password": self.page_reset.new_password_edit.text()}
            response = httpx.put(f"{self.url}/login/reset", json=payload)
            data = response.json()
            if data.get("message") == "OK":
                self.stackedWidget.setCurrentWidget(self.page_login)
                QMessageBox.warning(None,"Success", "Your password has been reset.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Connection Failed: {e}")


    def open_admin_management(self):
        self.page_admin.value_edit.setText("")
        self.page_admin.value_edit.setPlaceholderText("Enter Value")
        self.stackedWidget.setCurrentWidget(self.page_admin)


        self.previous_page_callback = self.open_admin_management

        self.admin_cards = []

        try :
            headers = {
                "Authorization": f"Bearer {self.jwt}"
            }
            response = httpx.get(f"{self.url}/admins/authenticate" , headers=headers)

            if response.status_code != 200:
                QMessageBox.warning(None, "Error", "Invalid Credentials")
                return

            if response.status_code == 403:
                QMessageBox.warning(None, "Error", "Only managers can access Admin Panel")
                return

            data = response.json()

            if not isinstance(data, list):
                QMessageBox.warning(None, "Error", "Unexpected response from server")
                return

            if not data :
                QMessageBox.warning(None, "Empty", "No information available")
                return


        except Exception as e:
            QMessageBox.critical(None, "Error", f"Connection Failed: {e}")
            return

        if self.page_admin.scroll_area.widget():
            self.page_admin.scroll_area.widget().deleteLater()

        self.page_admin.field_combo_box.clear()

        grid = QGridLayout()
        grid.setSpacing(20)

        row = 0
        col = 0

        #add fields names in to combo box
        columns = models.Admin.__table__.columns.keys()

        for key in columns:
            # if key != "password":
            self.page_admin.field_combo_box.addItem(str(key))


        for admin in data:
            card = RecordCard(admin)
            card.setMinimumWidth(300)

            card.select_radio.setChecked(False)
            self.radio_group.addButton(card.select_radio)

            self.admin_cards.append(card)

            grid.addWidget(card, row, col)

            col += 1
            if col >= 2:
                col = 0
                row += 1

        container = QWidget()
        container.setLayout(grid)

        self.page_admin.scroll_area.setWidget(container)
        self.page_admin.scroll_area.setWidgetResizable(True)


    def open_customers_page(self):
        self.page_customers.value_edit.setText("")
        self.page_customers.value_edit.setPlaceholderText("Enter Value")
        self.stackedWidget.setCurrentWidget(self.page_customers)

        self.previous_page_callback = self.open_customers_page

        self.customer_cards = []

        try:
            headers = {
                "Authorization": f"Bearer {self.jwt}"
            }
            response = httpx.get(f"{self.url}/customers/authenticate", headers=headers)

            if response.status_code != 200:
                QMessageBox.warning(None, "Error", "Invalid Credentials")
                return

            data = response.json()

            if not isinstance(data, list):
                QMessageBox.warning(None, "Error", "Unexpected response from server")
                return

            if not data :
                QMessageBox.warning(None, "Empty", "No information available")
                return


        except Exception as e:
            QMessageBox.critical(None, "Error", f"Connection Failed: {e}")
            return


        if self.page_customers.scroll_area.widget():
            self.page_customers.scroll_area.widget().deleteLater()

        self.page_customers.field_combo_box.clear()

        grid = QGridLayout()
        grid.setSpacing(20)

        row = 0
        col = 0

        columns = models.Customer.__table__.columns.keys()
        for key in columns:
            self.page_customers.field_combo_box.addItem(str(key))

        for customer in data:
            card = RecordCard(customer)
            card.setMinimumWidth(300)

            card.select_radio.setChecked(False)
            self.radio_group.addButton(card.select_radio)

            self.customer_cards.append(card)

            grid.addWidget(card, row, col)

            col += 1
            if col >= 2:
                col = 0
                row += 1

        container = QWidget()
        container.setLayout(grid)

        self.page_customers.scroll_area.setWidget(container)
        self.page_customers.scroll_area.setWidgetResizable(True)


    def open_products_page(self):
        self.page_products.value_edit.setText("")
        self.page_products.value_edit.setPlaceholderText("Enter Value")
        self.stackedWidget.setCurrentWidget(self.page_products)

        self.previous_page_callback = self.open_products_page

        self.product_cards = []

        try:
            headers = {
                "Authorization": f"Bearer {self.jwt}"
            }
            response = httpx.get(f"{self.url}/products/authenticate", headers=headers)

            if response.status_code != 200:
                QMessageBox.warning(None, "Error", "Invalid Credentials")
                return

            data = response.json()

            if not isinstance(data, list):
                QMessageBox.warning(None, "Error", "Unexpected response from server")
                return

            if not data :
                QMessageBox.warning(None, "Empty", "No information available")
                return

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Connection Failed: {e}")
            return


        if self.page_products.scroll_area.widget():
            self.page_products.scroll_area.widget().deleteLater()

        self.page_products.field_combo_box.clear()

        grid = QGridLayout()
        grid.setSpacing(20)

        row = 0
        col = 0

        columns = models.Product.__table__.columns.keys()
        for key in columns:
            self.page_products.field_combo_box.addItem(str(key))

        for product in data:
            if not product["stock"] :
                product["is_active"] = False
            card = RecordCard(product)
            card.setMinimumWidth(300)

            card.select_radio.setChecked(False)
            self.radio_group.addButton(card.select_radio)

            self.product_cards.append(card)

            grid.addWidget(card, row, col)

            col += 1
            if col >= 2:
                col = 0
                row += 1

        container = QWidget()
        container.setLayout(grid)

        self.page_products.scroll_area.setWidget(container)
        self.page_products.scroll_area.setWidgetResizable(True)


    def open_invoices_page(self):
        self.page_invoices.value_edit.setText("")
        self.page_invoices.value_edit.setPlaceholderText("Enter Value")
        self.stackedWidget.setCurrentWidget(self.page_invoices)

        self.previous_page_callback = self.open_invoices_page

        self.invoice_cards = []

        try:
            headers = {
                "Authorization": f"Bearer {self.jwt}"
            }
            response = httpx.get(f"{self.url}/invoices/authenticate", headers=headers)

            if response.status_code != 200:
                QMessageBox.warning(None, "Error", "Invalid Credentials")
                return

            data = response.json()

            if not isinstance(data, list):
                QMessageBox.warning(None, "Error", "Unexpected response from server")
                return

            if not data :
                QMessageBox.warning(None, "Empty", "No information available")
                return


        except Exception as e:
            QMessageBox.critical(None, "Error", f"Connection Failed: {e}")
            return


        if self.page_invoices.scroll_area.widget():
            self.page_invoices.scroll_area.widget().deleteLater()

        self.page_invoices.field_combo_box.clear()

        grid = QGridLayout()
        grid.setSpacing(20)

        row = 0
        col = 0

        columns = models.Invoice.__table__.columns.keys()
        for key in columns:
            self.page_invoices.field_combo_box.addItem(str(key))

        for invoice in data:
            card = RecordCard(invoice)
            card.setMinimumWidth(300)

            card.select_radio.setChecked(False)
            self.radio_group.addButton(card.select_radio)

            self.invoice_cards.append(card)

            grid.addWidget(card, row, col)

            col += 1
            if col >= 2:
                col = 0
                row += 1

        container = QWidget()
        container.setLayout(grid)

        self.page_invoices.scroll_area.setWidget(container)
        self.page_invoices.scroll_area.setWidgetResizable(True)


    def next_previous(self, direction: str, page):

        if self.previous_page_callback == self.open_admin_management:
            endpoint = "/admins"
        elif self.previous_page_callback == self.open_customers_page:
            endpoint = "/customers"
        elif self.previous_page_callback == self.open_products_page:
            endpoint = "/products"
        elif self.previous_page_callback == self.open_invoices_page:
            endpoint = "/invoices"
        else:
            return

        try:
            response = httpx.get(f"{self.url}{endpoint}/count")
            if response.status_code != 200:
                QMessageBox.critical(
                    None, "Error", f"Connection Failed: {response.status_code}"
                )
                return

            total = int(response.json().get("count", 0))

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Connection Failed: {e}")
            return

        if total == 0:
            self.skip = 0
            page.next_page_button.setEnabled(False)
            page.back_page_button.setEnabled(False)
            return

        max_skip = ((total - 1) // self.limit) * self.limit

        if direction == "n":  # next
            if self.skip < max_skip:
                self.skip += self.limit

        elif direction == "b":  # back
            if self.skip > 0:
                self.skip -= self.limit

        self.skip = max(0, min(self.skip, max_skip))

        BASE_DIR = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        ICONS_DIR = os.path.join(BASE_DIR, "Icons")

        disabled_right = os.path.join(ICONS_DIR, "arrow_circle_right_100dp_999999.png")
        enabled_right = os.path.join(ICONS_DIR, "arrow_circle_right_100dp_FFFFFF.png")
        disabled_left = os.path.join(ICONS_DIR, "arrow_circle_left_100dp_999999.png")
        enabled_left = os.path.join(ICONS_DIR, "arrow_circle_left_100dp_FFFFFF.png")

        if self.skip >= max_skip:
            page.next_page_button.setEnabled(False)
            page.next_page_button.setIcon(QIcon(disabled_right))
        else:
            page.next_page_button.setEnabled(True)
            page.next_page_button.setIcon(QIcon(enabled_right))

        if self.skip <= 0:
            page.back_page_button.setEnabled(False)
            page.back_page_button.setIcon(QIcon(disabled_left))
        else:
            page.back_page_button.setEnabled(True)
            page.back_page_button.setIcon(QIcon(enabled_left))

        self.filtered_result()


    def filtered_result(self):
        if self.previous_page_callback == self.open_admin_management :
            # if not self.page_admin.value_edit.text().strip()  :
            #     QMessageBox.critical(None, "Error", "Complete your filter value")
            #     return

            self.admin_cards = []

            field = self.page_admin.field_combo_box.currentText().strip()
            value = self.page_admin.value_edit.text().strip()


            if value :
                params = {field: value, "skip": self.skip}

            else :
                params = {"skip": self.skip}

            # params = {field: value , "skip" : self.skip  }
            try :
                response = httpx.get(f"{self.url}/admins/filter" , params=params)
                if response.status_code != 200 :
                    QMessageBox.critical(None, "Error", f"Connection Failed: {response.status_code}")
                    return

                data = response.json()

                if not data:
                    QMessageBox.information(None, "Result", "No matching results found.")
                    return


            except Exception as e:
                QMessageBox.critical(None, "Error", f"Connection Failed: {e}")
                return

            if self.page_admin.scroll_area.widget():
                self.page_admin.scroll_area.widget().deleteLater()

            grid = QGridLayout()
            grid.setSpacing(20)

            row = 0
            col = 0

            for admin in data:
                card = RecordCard(admin)
                card.setMinimumWidth(300)

                grid.addWidget(card, row, col)

                col += 1
                if col >= 2:
                    col = 0
                    row += 1

                self.admin_cards.append(card)

            container = QWidget()
            container.setLayout(grid)

            self.page_admin.scroll_area.setWidget(container)
            self.page_admin.scroll_area.setWidgetResizable(True)


        if self.previous_page_callback == self.open_customers_page:

            self.customer_cards = []

            field = self.page_customers.field_combo_box.currentText().strip()
            value = self.page_customers.value_edit.text().strip()


            if value :
                params = {field: value, "skip": self.skip}

            else :
                params = {"skip": self.skip}

            # params = {field: value , "skip" : self.skip  }
            try :
                response = httpx.get(f"{self.url}/customers/filter" , params=params)
                if response.status_code != 200 :
                    QMessageBox.critical(None, "Error", f"Connection Failed: {response.status_code}")
                    return

                data = response.json()

                if not data:
                    QMessageBox.information(None, "Result", "No matching results found.")
                    return


            except Exception as e:
                QMessageBox.critical(None, "Error", f"Connection Failed: {e}")
                return

            if self.page_customers.scroll_area.widget():
                self.page_customers.scroll_area.widget().deleteLater()

            grid = QGridLayout()
            grid.setSpacing(20)

            row = 0
            col = 0

            for customer in data:
                card = RecordCard(customer)
                card.setMinimumWidth(300)

                grid.addWidget(card, row, col)

                col += 1
                if col >= 2:
                    col = 0
                    row += 1

                self.customer_cards.append(card)

            container = QWidget()
            container.setLayout(grid)

            self.page_customers.scroll_area.setWidget(container)
            self.page_customers.scroll_area.setWidgetResizable(True)


        if self.previous_page_callback == self.open_invoices_page:

            self.invoice_cards = []

            field = self.page_invoices.field_combo_box.currentText().strip()
            value = self.page_invoices.value_edit.text().strip()


            if value :
                params = {field: value, "skip": self.skip}

            else :
                params = {"skip": self.skip}

            # params = {field: value , "skip" : self.skip  }
            try :
                response = httpx.get(f"{self.url}/invoices/filter" , params=params)
                if response.status_code != 200 :
                    QMessageBox.critical(None, "Error", f"Connection Failed: {response.status_code}")
                    return

                data = response.json()

                if not data:
                    QMessageBox.information(None, "Result", "No matching results found.")
                    return


            except Exception as e:
                QMessageBox.critical(None, "Error", f"Connection Failed: {e}")
                return

            if self.page_invoices.scroll_area.widget():
                self.page_invoices.scroll_area.widget().deleteLater()

            grid = QGridLayout()
            grid.setSpacing(20)

            row = 0
            col = 0

            for invoice in data:
                card = RecordCard(invoice)
                card.setMinimumWidth(300)

                grid.addWidget(card, row, col)

                col += 1
                if col >= 2:
                    col = 0
                    row += 1

                self.invoice_cards.append(card)

            container = QWidget()
            container.setLayout(grid)

            self.page_invoices.scroll_area.setWidget(container)
            self.page_invoices.scroll_area.setWidgetResizable(True)


        if self.previous_page_callback == self.open_products_page:

            self.product_cards = []

            field = self.page_products.field_combo_box.currentText().strip()
            value = self.page_products.value_edit.text().strip()


            if value :
                params = {field: value, "skip": self.skip}

            else :
                params = {"skip": self.skip}

            try :
                headers = {
                    "Authorization": f"Bearer {self.jwt}"
                }
                response = httpx.get(f"{self.url}/products/filter" , params=params , headers=headers)
                if response.status_code != 200 :
                    QMessageBox.critical(None, "Error", f"Connection Failed: {response.status_code}")
                    return

                data = response.json()

                if not data:
                    QMessageBox.information(None, "Result", "No matching results found.")
                    return


            except Exception as e:
                QMessageBox.critical(None, "Error", f"Connection Failed: {e}")
                return

            if self.page_products.scroll_area.widget():
                self.page_products.scroll_area.widget().deleteLater()

            grid = QGridLayout()
            grid.setSpacing(20)

            row = 0
            col = 0

            for product in data:
                card = RecordCard(product)
                card.setMinimumWidth(300)

                grid.addWidget(card, row, col)

                col += 1
                if col >= 2:
                    col = 0
                    row += 1

                self.product_cards.append(card)

            container = QWidget()
            container.setLayout(grid)

            self.page_products.scroll_area.setWidget(container)
            self.page_products.scroll_area.setWidgetResizable(True)


    def open_add_records_page(self):

        self.stackedWidget.setCurrentWidget(self.page_add_records)

        if self.page_add_records.scroll_area.widget():
            self.page_add_records.scroll_area.widget().deleteLater()

        grid = QGridLayout()
        grid.setSpacing(20)

        row = 0
        col = 0

        if self.previous_page_callback == self.open_admin_management :
            columns = models.Admin.__table__.columns.keys()

        elif self.previous_page_callback == self.open_customers_page :
            columns = models.Customer.__table__.columns.keys()

        elif self.previous_page_callback == self.open_products_page :
            columns = models.Product.__table__.columns.keys()

        elif self.previous_page_callback == self.open_invoices_page :
            columns = models.Invoice.__table__.columns.keys()

        self.card = AddCard(columns)
        self.card.setMinimumWidth(300)

        grid.addWidget(self.card, row, col)

        col += 1
        if col >= 2:
            col = 0
            row += 1

        container = QWidget()
        container.setLayout(grid)

        self.page_add_records.scroll_area.setWidget(container)
        self.page_add_records.scroll_area.setWidgetResizable(True)


    def submit_add_records(self):
        if self.previous_page_callback == self.open_admin_management :
            endpoint = "/admins/create"

        elif self.previous_page_callback == self.open_customers_page :
            endpoint = "/customers/create"

        elif self.previous_page_callback == self.open_products_page :
            endpoint = "/products/create"

        elif self.previous_page_callback == self.open_invoices_page :
            endpoint = "/invoices/create"

        values = {}
        empty = []
        for field, widget in self.card.inputs.items():
            if widget.text().strip():
                values[field] = widget.text().strip()
            else :
                empty.append(field)

        try:
            headers = {
                "Authorization": f"Bearer {self.jwt}"
            }
            response = httpx.post(f"{self.url}{endpoint}", json=values , headers=headers)

            if response.status_code == 201:
                QMessageBox.information(None, "Success", "Record added successfully!")
                self.previous_page_callback()

            else:
                QMessageBox.warning(None, "Error", f"Failed: {response.text}")

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Connection failed: {e}")


    def open_edit_records_page(self,page):
        selected = None

        if page == "Admin" :
            cards = self.admin_cards

        elif page == "Customer" :
            cards = self.customer_cards

        elif page == "Product" :
            cards = self.product_cards

        elif page == "Invoice" :
            cards = self.invoice_cards

        for card in cards:
            if card.select_radio.isChecked():
                selected = card.record_data

        if not selected:
            QMessageBox.warning(None, "Error", "Please select one record.")
            return

        self.stackedWidget.setCurrentWidget(self.page_edit_records)
        if self.page_edit_records.scroll_area.widget():
            self.page_edit_records.scroll_area.widget().deleteLater()


        self.edit_card = EditCard(selected)

        container = QWidget()
        v = QVBoxLayout()
        v.addWidget(self.edit_card)
        container.setLayout(v)

        self.page_edit_records.scroll_area.setWidget(container)
        self.page_edit_records.scroll_area.setWidgetResizable(True)

        self.stackedWidget.setCurrentWidget(self.page_edit_records)


    def submit_edit_records_page(self):

        if self.previous_page_callback == self.open_admin_management :
            endpoint = "/admins/update/"

        elif self.previous_page_callback == self.open_customers_page:
            endpoint = "/customers/update/"

        elif self.previous_page_callback == self.open_products_page :
            endpoint = "/products/update/"

        elif self.previous_page_callback == self.open_invoices_page :
            endpoint = "/invoices/update/"

        updated_values = self.edit_card.get_updated_values()

        record_id = updated_values.get("id")

        try:
            res = httpx.put(
                f"{self.url}{endpoint}{record_id}",
                json=updated_values
            )
            data = res.json()

            if res.status_code == 422:
                QMessageBox.warning(None, "Error", "Field Values is not Valid!")
                return

            elif data.get("message") == "OK":
                QMessageBox.information(None, "Success", "Record updated.")
                self.previous_page_callback()

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed: {e}")


    def delete_record(self):
        selected_id = None

        cards_list = []
        if self.previous_page_callback == self.open_admin_management:
            cards_list = self.admin_cards
            endpoint = "admins/delete"

        elif self.previous_page_callback == self.open_customers_page:
            cards_list = self.customer_cards
            endpoint = "customers/delete"

        elif self.previous_page_callback == self.open_products_page:
            cards_list = self.product_cards
            endpoint = "products/delete"

        elif self.previous_page_callback == self.open_invoices_page:
            cards_list = self.invoice_cards
            endpoint = "invoices/delete"

        for item in cards_list:
            if item["radio"].isChecked():
                selected_id = item["id"]

        if not selected_id:
            QMessageBox.warning(self, "Warning", "No records selected!")
            return

        try:
            headers = {
                "Authorization": f"Bearer {self.jwt}"
            }
            response = httpx.delete(
                f"{self.url}/{endpoint}/{selected_id}" , headers=headers)


            if response.status_code == 204:
                QMessageBox.information(self, "Success", f"Record deleted successfully.")

                self.stackedWidget.setCurrentWidget( self.previous_page_callback)


            else:
                QMessageBox.warning(self, "Error", "Failed to delete the selected records.")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Could not connect to the server:\n{e}")


    def open_reports_page(self):
        self.stackedWidget.setCurrentWidget(self.page_reports)

        # old_widget = self.page_reports.scroll_area.takeWidget()
        # if old_widget:
        #     old_widget.deleteLater()

        current = QDateTime.currentDateTime()
        self.page_reports.to_time.setDateTime(current)
        self.page_reports.from_time.setDateTime(current.addDays(-7))


    def create_report_card(self, title: str, value: str, description: str = ""):
        card = QWidget()
        card.setFixedWidth(300)
        card.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3d2b6b, stop:1 #2a1f4d);
                border-radius: 18px;
                border: 2px solid #6a5acd;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #e6d9ff; font-size: 16px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)

        value_label = QLabel(value)
        value_label.setStyleSheet("color: #ffffff; font-size: 30px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        if description:
            desc_label = QLabel(description)
            desc_label.setStyleSheet("color: #b19bff; font-size: 13px;")
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        return card


    def show_reports(self):
        from_datetime = self.page_reports.from_time.dateTime().toPyDateTime()
        to_datetime = self.page_reports.to_time.dateTime().toPyDateTime()

        if from_datetime > to_datetime:
            QMessageBox.warning(self, "Error", "Start date cannot be later than end date!")
            return

        try:
            headers = {"Authorization": f"Bearer {self.jwt}"}
            payload = {
                "from_time": from_datetime.isoformat(),
                "to_time": to_datetime.isoformat()
            }

            response = httpx.post(
                f"{self.url}/reports/get",
                headers=headers,
                json=payload
            )

            if response.status_code != 200:
                QMessageBox.warning(self, "Error", "Failed to fetch reports")
                return

            data = response.json()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection failed:\n{e}")
            return

        old_widget = self.page_reports.scroll_area.takeWidget()
        if old_widget:
            old_widget.deleteLater()

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setAlignment(Qt.AlignTop)

        def add_row(*cards):
            row = QHBoxLayout()
            row.setSpacing(20)
            row.setAlignment(Qt.AlignCenter)
            for card in cards:
                row.addWidget(card)
            main_layout.addLayout(row)

        add_row(
            self.create_report_card(
                "Invoices Count",
                str(data.get("invoices_count", 0)),
                "Total invoices"
            ),
            self.create_report_card(
                "Total Paid",
                f"{data.get('total_paid', 0):,.0f}",
                "Total revenue"
            )
        )

        add_row(
            self.create_report_card(
                "Average Invoice",
                f"{data.get('average_paid', 0):,.0f}",
                "Average per invoice"
            ),
            self.create_report_card(
                "Customers Count",
                str(data.get("customers_count", 0)),
                "Unique customers"
            )
        )

        if data.get("best_customer"):
            bc = data["best_customer"]
            add_row(
                self.create_report_card(
                    "Best Customer",
                    f"ID: {bc['customer_id']}",
                    f"Total Paid: {bc['total_paid']:,.0f}"
                )
            )

        if data.get("most_sold_product"):
            mp = data["most_sold_product"]
            add_row(
                self.create_report_card(
                    "Most Sold Product",
                    f"Product ID: {mp['product_id']}",
                    f"Sold: {mp['total_sold']}"
                )
            )

        if data.get("max_paid"):
            max_inv = data["max_paid"]
            add_row(
                self.create_report_card(
                    "Highest Invoice",
                    f"{max_inv['total_paid']:,.0f}",
                    f"Invoice ID: {max_inv['invoice_id']}"
                )
            )

        if data.get("min_paid"):
            min_inv = data["min_paid"]
            add_row(
                self.create_report_card(
                    "Lowest Invoice",
                    f"{min_inv['total_paid']:,.0f}",
                    f"Invoice ID: {min_inv['invoice_id']}"
                )
            )

        add_row(
            self.create_report_card(
                "Average Items per Invoice",
                f"{data.get('average_item_invoice', 0):.1f}",
                "Items per invoice"
            )
        )

        self.page_reports.scroll_area.setWidgetResizable(True)
        self.page_reports.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.page_reports.scroll_area.setWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Home()
    window.show()
    sys.exit(app.exec_())