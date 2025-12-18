# Store Management System 🏪

A powerful full-stack desktop application for retail store management. Built with **FastAPI** backend and **PyQt5** modern GUI – featuring inventory tracking, invoicing with automatic discounts, customer levels, and comprehensive reports.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Modern_API-brightgreen)
![PyQt5](https://img.shields.io/badge/PyQt5-Desktop_GUI-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Docker](https://img.shields.io/badge/Docker-Fully_Supported-success)

## 🚀 Features
- Secure JWT authentication with Argon2 password hashing
- Role-based access control (Manager / Employee)
- Customer management with automatic discount tiers based on purchase history
- Real-time product stock management with automatic updates
- Invoice system with discount calculation, stock rollback on deletion
- Advanced search, filtering, and pagination
- Detailed time-range analytical reports (total sales, average, best customer, top product)
- Beautiful, responsive desktop interface using PyQt5
- Full Docker support for easy setup and deployment

## 🖼️ Screenshots

<div align="center">

![Login Screen](https://github.com/iphosein/Store-Management-System/blob/c75ae8ce425ef9b3b74e761df0330449895303a8/screenshots/Login.JPG)
![Home Dashboard](https://github.com/iphosein/Store-Management-System/blob/c75ae8ce425ef9b3b74e761df0330449895303a8/screenshots/Home.JPG)
![Customers Management](https://github.com/iphosein/Store-Management-System/blob/c75ae8ce425ef9b3b74e761df0330449895303a8/screenshots/Customers_Page.JPG)
![Invoices List](https://github.com/iphosein/Store-Management-System/blob/c75ae8ce425ef9b3b74e761df0330449895303a8/screenshots/Invoices_Page.JPG)
![Add New Record](https://github.com/iphosein/Store-Management-System/blob/c75ae8ce425ef9b3b74e761df0330449895303a8/screenshots/Add_Record.JPG)
![Forgot Password](https://github.com/iphosein/Store-Management-System/blob/c75ae8ce425ef9b3b74e761df0330449895303a8/screenshots/Forget.JPG)
![Reset Password](https://github.com/iphosein/Store-Management-System/blob/c75ae8ce425ef9b3b74e761df0330449895303a8/screenshots/Reset_pass.JPG)

</div>

## 🛠️ Tech Stack
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Alembic
- **Frontend**: PyQt5
- **Auth**: JWT (python-jose), Argon2 (passlib)
- **Containerization**: Docker & Docker Compose

## 📦 Quick Start

### Recommended: Run with Docker (One command!)
```bash
git clone https://github.com/iphosein/store-management-system.git
cd store-management-system

docker-compose up --build
