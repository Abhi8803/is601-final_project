# IS601 Final Project – Dosa Restaurant API

## Project Description

For this final project, I created a REST API backend for a dosa restaurant using FastAPI and SQLite. The goal of the program is to provide a fully functional API that allows the restaurant to manage customers, menu items, and orders through standard HTTP requests.

The program reads an orders file and produces:
* **db.sqlite** – a relational database containing customers, items, orders, and order_items tables
* **REST API** – a FastAPI backend that supports full CRUD operations on all three objects

---

## How the Program Works

1. The program reads `example_orders.json` containing 10,001 restaurant orders.
2. It extracts unique customers and menu items, deduplicating as it goes.
3. It seeds a SQLite database with proper primary and foreign key constraints.
4. The FastAPI backend reads and writes from `db.sqlite` to handle all API requests.

This allows the restaurant to create, read, update, and delete customer records, menu items, and orders through a clean REST API.

---

## Input File

The input file is a JSON file that contains a list of orders. Each order includes:
* Customer name and phone number
* A list of items ordered with prices
* A timestamp and optional notes

Example:
```json
{
  "timestamp": 1702219784,
  "name": "Damodhar",
  "phone": "732-555-5509",
  "items": [
    {
      "name": "Cheese Madurai Masala Dosa",
      "price": 13.95
    }
  ],
  "notes": "extra spicy"
}
```

---

## Database Schema

### customers
Stores unique customers extracted from the orders.
```json
{
  "id": 1,
  "name": "Damodhar",
  "phone": "732-555-5509"
}
```

### items
Stores unique menu items extracted from the orders.
```json
{
  "id": 1,
  "name": "Cheese Madurai Masala Dosa",
  "price": 13.95
}
```

### orders
Stores each order linked to a customer.
```json
{
  "id": 1,
  "customer_id": 1,
  "timestamp": 1702219784,
  "notes": "extra spicy"
}
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/customers` | Create a new customer |
| GET | `/customers/{id}` | Get a customer by ID |
| PUT | `/customers/{id}` | Update a customer by ID |
| DELETE | `/customers/{id}` | Delete a customer by ID |
| POST | `/items` | Create a new menu item |
| GET | `/items/{id}` | Get an item by ID |
| PUT | `/items/{id}` | Update an item by ID |
| DELETE | `/items/{id}` | Delete an item by ID |
| POST | `/orders` | Create a new order |
| GET | `/orders/{id}` | Get an order by ID |
| PUT | `/orders/{id}` | Update an order by ID |
| DELETE | `/orders/{id}` | Delete an order by ID |

---

## How to Run the Program

Navigate to the project folder and activate the virtual environment.

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install "fastapi[standard]"
```

Initialize the database.

```bash
python3 init_db.py
```

After running the program, the following will be created:
* `db.sqlite` – seeded with 31 customers, 19 items, and 10,001 orders

Start the development server.

```bash
fastapi dev main.py
```

The API will be running at `http://127.0.0.1:8000` and interactive docs at `http://127.0.0.1:8000/docs`.

---

## Design Approach

I organized the program using a context manager to handle database connections cleanly and safely. Pydantic models are used for request validation and response serialization, keeping the API type-safe and self-documenting.

I used SQLite's `PRAGMA foreign_keys = ON` to enforce relational constraints between tables, and `AUTOINCREMENT` primary keys so IDs are assigned automatically by the database.

---

## Technologies Used

* Python 3
* FastAPI
* SQLite
* Pydantic
* Git and GitHub

---

Abhiram Panuganti (ap3364)
ap3364@njit.edu