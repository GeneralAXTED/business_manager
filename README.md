# 📊 Telegram Business Manager

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-green.svg)](https://docs.aiogram.dev/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)

A lightweight, modular **Telegram Bot mini-ERP system** built with **Python** and **Aiogram 3.x**. This project allows small business owners and managers to handle daily operations—such as inventory, customer tracking, sales, debts, and financial reporting—directly through a Telegram interface.

---

## 🚀 Key Features

*   📦 **Inventory Management (Ombor):** Add new products, monitor stock levels in real-time, and view product lists.
*   👥 **Customer Database (Mijozlar bazasi):** Easily register new customers with their names and phone numbers.
*   🛒 **Order & Sales Processing (Buyurtmalar):** Process sales seamlessly, automatically update warehouse stock quantities, and generate order check receipts.
*   💳 **Debt Management (Qarzdorlik):** Track customer debts, record partial or full payments, and view a consolidated summary of outstanding balances.
*   📊 **Financial Reports (Hisobot):** Generate instant daily and monthly sales turnover summaries using built-in database queries.

---

## 📂 Project Architecture

The project is structured using a clean modular architecture (Routers) to ensure maintainability and scalability:

```text
business_manager/
│
├── database.py       # SQLite database configuration and queries
├── bot.py            # Main entry point to initialize and start the bot
├── requirements.txt  # Project dependencies
│
└── handlers/         # Modular command and callback routers
    ├── __init__.py   # Package initializer
    ├── common.py     # /start, /cancel commands and main keyboard layout
    ├── ombor.py      # Inventory module (FSM-based product creation & stock view)
    ├── mijozlar.py   # Customer module (Customer registration & list view)
    ├── buyurtma.py   # Order/Sales module (Transactions & stock deduction)
    ├── qarzdorlik.py # Debt module (Debt tracking, creation, and payment)
    └── hisobot.py    # Financial reporting module (Daily & monthly summaries)