from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey , Numeric , Text , Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, date
from .database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    gender = Column(String(20))
    birth_day = Column(Date)
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    total_purchases = Column(Integer, default=0)
    level = Column(Integer, default=0)
    first_purchase_date = Column(Date , default=date.today())

    invoices = relationship("Invoice", back_populates="customer")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=False)
    # username = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50) , nullable=False)
    last_name = Column(String(50) , nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    # password_hint = Column(String(200))
    national_id = Column(String(20), unique=True)
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    education = Column(String(100))
    hire_date = Column(Date, default=date.today())
    role = Column(String(50) , nullable=False)
    gender = Column(String(10))
    birth_date = Column(Date)
    # age = Column(Integer)
    salary = Column(Integer)

    invoices = relationship("Invoice", back_populates="admin")

    @hybrid_property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                        (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100) , nullable=False)
    stock = Column(Integer, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    invoice_items = relationship("InvoiceItem", back_populates="product")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("admins.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    purchase_date = Column(DateTime, default=func.now())
    total_paid = Column(Numeric(12, 2) )
    discount_amount = Column(Numeric(12, 2) )
    b_list = Column(String, nullable=False)

    admin = relationship("Admin", back_populates="invoices")
    customer = relationship("Customer", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice" , cascade="all, delete")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Numeric(12, 2), nullable=False)

    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product", back_populates="invoice_items")