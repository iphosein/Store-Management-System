from pydantic import BaseModel , EmailStr
from datetime import  date , datetime
from typing import Optional
from decimal import Decimal
from pydantic.types import conint


class Forget(BaseModel):
    email : EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    model_config = {
        "from_attributes": True
    }

class ResetPassword(BaseModel):
    email: EmailStr
    password: str
###########################################################
class ProductUpdate(BaseModel):
    id: Optional[int]
    name: Optional[str]
    stock: Optional[int]
    price: Optional[float]
    description: Optional[str]
    is_active: Optional[bool]
    model_config = {
        "from_attributes": True
    }

class ProductOut(BaseModel):
    id: int
    name: str
    stock: int
    price: float
    description: str
    is_active: bool
    model_config = {
        "from_attributes": True
    }

class CreateProduct(BaseModel):
    name: str
    stock: int
    price: float
    description: str
    # is_active: Optional[bool]
    model_config = {
        "from_attributes": True
    }

#######################################################

class CreateList(BaseModel):
    invoice_id: int
    product_id: int
    quantity: int
    model_config = {
        "from_attributes": True
    }

class GetList(BaseModel):
    # invoice_id: int
    product_id: int
    quantity: int
    model_config = {
        "from_attributes": True
    }

#######################################################

class GetReport(BaseModel):
    from_time : datetime
    to_time : datetime


class ReportOut(BaseModel):
    invoices_count: int
    total_paid: float
    average_paid: float
    customers_count: int
    max_paid: Optional[dict]
    min_paid: Optional[dict]
    best_customer: Optional[dict]
    average_item_invoice: float
    most_sold_product: Optional[dict]

#######################################################
class InvoiceOut(BaseModel):
    id : int
    admin_id : int
    customer_id: int
    purchase_date : datetime
    b_list : str
    total_paid: Decimal
    discount_amount: Decimal
    model_config = {
        "from_attributes": True
    }

class InvoiceUpdate(BaseModel):
    admin_id: Optional[int]
    customer_id: Optional[int]
    purchase_date: Optional[datetime]
    b_list : Optional[str]
    total_paid: Optional[Decimal]
    discount_amount: Optional[Decimal]
    model_config = {
        "from_attributes": True
    }

class CreateInvoice(BaseModel):
    admin_id : Optional[int] = None
    customer_id: int
    # purchase_date : Optional[date]
    b_list : str
    # total_paid: Optional[Decimal]
    # discount_amount: Optional[Decimal]
    model_config = {
        "from_attributes": True
    }

###########################################################

class CustomerUpdate(BaseModel):
    id : int
    phone_number :int
    first_name : str
    last_name : str
    gender : str
    birth_day : date
    city : str
    state : str
    country : str
    total_purchases : float
    level : conint(ge=0, le=3)
    first_purchase_date : date
    model_config = {
        "from_attributes": True
    }

class CustomerOut(BaseModel):
    id : int
    phone_number : int
    first_name : str
    last_name : str
    gender: str
    birth_day: date
    city : str
    state : str
    country : str
    total_purchases : float
    level : conint(ge=0, le=3)
    first_purchase_date : date
    model_config = {
        "from_attributes": True
    }

class CreateCustomer(BaseModel):
    phone_number : int
    first_name : str
    last_name : str
    gender: str
    birth_day: date
    city : str
    state : str
    country : str
    total_purchases : Optional[int] = 0
    #level : conint(ge=0, le=3)
    #first_purchase_date : Optional[date]
    model_config = {
        "from_attributes": True
    }

###########################################################

class AdminCreate(BaseModel):
    phone_number : int
    first_name : str
    last_name : str
    email : EmailStr
    password :str
    national_id : int
    city : str
    state : str
    country : str
    education : str
    hire_date : Optional[date]
    role : str
    gender : str
    birth_date : date
    # age : Optional[int]
    salary : int

    model_config = {
        "from_attributes": True
    }

class UpdateAdmin(BaseModel):
    id : int
    phone_number: int
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    national_id: int
    city: str
    state: str
    country: str
    education: str
    hire_date: Optional[date]
    role: str
    gender: str
    birth_date: date
    salary: int

    model_config = {
        "from_attributes": True
    }

class AdminOut(BaseModel):
    id : int
    phone_number : int
    first_name : str
    last_name : str
    email : EmailStr
    password :str
    national_id : int
    city : str
    state : str
    country : str
    education : str
    hire_date : Optional[date]
    role : str
    gender : str
    birth_date : date
    age : Optional[int]
    salary : int

    model_config = {
        "from_attributes": True
    }

###########################################################

class Token(BaseModel):
    access_token: str
    token_type: str
    name : str

class TokenData(BaseModel):
    id: Optional[int] = None
