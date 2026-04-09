import sqlite3
from contextlib import contextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_PATH = "db.sqlite"

app = FastAPI(title="Dosa Restaurant API")


# ------------------------------------------------------------------ #
# DB helper                                                            #
# ------------------------------------------------------------------ #

@contextmanager
def get_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


# ------------------------------------------------------------------ #
# Pydantic models                                                      #
# ------------------------------------------------------------------ #

class CustomerIn(BaseModel):
    name: str
    phone: str

class CustomerOut(CustomerIn):
    id: int


class ItemIn(BaseModel):
    name: str
    price: float

class ItemOut(ItemIn):
    id: int


class OrderIn(BaseModel):
    customer_id: int
    timestamp: Optional[int] = None
    notes: Optional[str] = ""

class OrderOut(OrderIn):
    id: int


# ------------------------------------------------------------------ #
# Customers                                                            #
# ------------------------------------------------------------------ #

@app.post("/customers", response_model=CustomerOut, status_code=201)
def create_customer(customer: CustomerIn):
    with get_db() as con:
        cur = con.execute(
            "INSERT INTO customers (name, phone) VALUES (?, ?)",
            (customer.name, customer.phone),
        )
        return CustomerOut(id=cur.lastrowid, **customer.model_dump())


@app.get("/customers/{id}", response_model=CustomerOut)
def get_customer(id: int):
    with get_db() as con:
        row = con.execute("SELECT * FROM customers WHERE id = ?", (id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerOut(**row)


@app.put("/customers/{id}", response_model=CustomerOut)
def update_customer(id: int, customer: CustomerIn):
    with get_db() as con:
        cur = con.execute(
            "UPDATE customers SET name = ?, phone = ? WHERE id = ?",
            (customer.name, customer.phone, id),
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerOut(id=id, **customer.model_dump())


@app.delete("/customers/{id}", status_code=204)
def delete_customer(id: int):
    with get_db() as con:
        cur = con.execute("DELETE FROM customers WHERE id = ?", (id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Customer not found")


# ------------------------------------------------------------------ #
# Items                                                                #
# ------------------------------------------------------------------ #

@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(item: ItemIn):
    with get_db() as con:
        cur = con.execute(
            "INSERT INTO items (name, price) VALUES (?, ?)",
            (item.name, item.price),
        )
        return ItemOut(id=cur.lastrowid, **item.model_dump())


@app.get("/items/{id}", response_model=ItemOut)
def get_item(id: int):
    with get_db() as con:
        row = con.execute("SELECT * FROM items WHERE id = ?", (id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemOut(**row)


@app.put("/items/{id}", response_model=ItemOut)
def update_item(id: int, item: ItemIn):
    with get_db() as con:
        cur = con.execute(
            "UPDATE items SET name = ?, price = ? WHERE id = ?",
            (item.name, item.price, id),
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
    return ItemOut(id=id, **item.model_dump())


@app.delete("/items/{id}", status_code=204)
def delete_item(id: int):
    with get_db() as con:
        cur = con.execute("DELETE FROM items WHERE id = ?", (id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")


# ------------------------------------------------------------------ #
# Orders                                                               #
# ------------------------------------------------------------------ #

@app.post("/orders", response_model=OrderOut, status_code=201)
def create_order(order: OrderIn):
    with get_db() as con:
        # verify customer exists
        if not con.execute("SELECT 1 FROM customers WHERE id = ?", (order.customer_id,)).fetchone():
            raise HTTPException(status_code=404, detail="Customer not found")
        cur = con.execute(
            "INSERT INTO orders (customer_id, timestamp, notes) VALUES (?, ?, ?)",
            (order.customer_id, order.timestamp, order.notes),
        )
        return OrderOut(id=cur.lastrowid, **order.model_dump())


@app.get("/orders/{id}", response_model=OrderOut)
def get_order(id: int):
    with get_db() as con:
        row = con.execute("SELECT * FROM orders WHERE id = ?", (id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderOut(**row)


@app.put("/orders/{id}", response_model=OrderOut)
def update_order(id: int, order: OrderIn):
    with get_db() as con:
        if not con.execute("SELECT 1 FROM customers WHERE id = ?", (order.customer_id,)).fetchone():
            raise HTTPException(status_code=404, detail="Customer not found")
        cur = con.execute(
            "UPDATE orders SET customer_id = ?, timestamp = ?, notes = ? WHERE id = ?",
            (order.customer_id, order.timestamp, order.notes, id),
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found")
    return OrderOut(id=id, **order.model_dump())


@app.delete("/orders/{id}", status_code=204)
def delete_order(id: int):
    with get_db() as con:
        cur = con.execute("DELETE FROM orders WHERE id = ?", (id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found")
