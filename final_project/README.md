# Dosa Restaurant API

A REST API backend for a dosa restaurant, built with FastAPI and SQLite. Supports full CRUD for customers, items, and orders.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install "fastapi[standard]"
python init_db.py
fastapi dev main.py
```

Open http://127.0.0.1:8000/docs for Swagger UI or open index.html for the custom API explorer.

## Endpoints

- POST/GET/PUT/DELETE /customers
- POST/GET/PUT/DELETE /items
- POST/GET/PUT/DELETE /orders

## Schema

- customers (id, name, phone)
- items (id, name, price)
- orders (id, customer_id, timestamp, notes)
- order_items (id, order_id, item_id)
