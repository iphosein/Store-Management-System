from fastapi import FastAPI
from . import models
from .database import engine
from .routers import customer , admin , auth , product , invoice , buy_list , reports

from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind = engine)
app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(customer.router)
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(invoice.router)
# app.include_router(buy_list.router)
app.include_router(reports.router)

# @app.get("/")
# def root():
#     return {"message": "Hello World pushing out to ubuntu"}
