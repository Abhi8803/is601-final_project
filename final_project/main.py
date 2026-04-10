import sqlite3
from contextlib import contextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse, RedirectResponse # pyright: ignore[reportMissingImports]
from pydantic import BaseModel # pyright: ignore[reportMissingImports]

DB_PATH = "db.sqlite"

app = FastAPI(
    title="Dosa Restaurant API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)


# ------------------------------------------------------------------ #
# Root redirect                                                        #
# ------------------------------------------------------------------ #

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


# ------------------------------------------------------------------ #
# Custom dark Swagger UI                                               #
# ------------------------------------------------------------------ #

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
  <title>Dosa Restaurant API</title>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.11.0/swagger-ui.min.css">
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; background: #0a0a0a; }
    .swagger-ui .topbar { background: #0a0a0a; border-bottom: 1px solid #1f1f1f; padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; }
    .swagger-ui .topbar .download-url-wrapper { display: none; }
    .swagger-ui .topbar .topbar-wrapper img { display: none; }
    .swagger-ui .topbar .topbar-wrapper a { display: none; }
    .swagger-ui .topbar-wrapper { display: flex; align-items: center; justify-content: space-between; width: 100%; }
    .swagger-ui .topbar-wrapper::before {
      content: 'Dosa Restaurant API';
      font-family: 'Times New Roman', Times, serif;
      font-size: 20px;
      font-style: italic;
      color: #e8834a;
      letter-spacing: 0.02em;
      flex: 1;
    }
    .swagger-ui .topbar-wrapper::after {
      content: 'Abhiram Panuganti (ap3364)  ·  ap3364@njit.edu';
      font-family: 'Times New Roman', Times, serif;
      font-size: 13px;
      color: #888;
      letter-spacing: 0.02em;
    }
    .swagger-ui { background: #0a0a0a; color: #d4d0c8; font-family: 'Helvetica Neue', sans-serif; }
    .swagger-ui .wrapper { background: #0a0a0a; }
    .swagger-ui .info { display: none; }
    .swagger-ui .scheme-container { background: #0f0f0f; border-bottom: 1px solid #1f1f1f; box-shadow: none; }
    .swagger-ui .opblock { background: #111; border: 1px solid #1f1f1f; border-radius: 6px; margin-bottom: 8px; box-shadow: none; }
    .swagger-ui .opblock .opblock-summary { border-bottom: 1px solid #1f1f1f; }
    .swagger-ui .opblock .opblock-summary-description { color: #888; font-size: 13px; }
    .swagger-ui .opblock .opblock-summary-path { color: #d4d0c8; font-family: 'Courier New', monospace; font-size: 14px; }
    .swagger-ui .opblock .opblock-body { background: #0d0d0d; }
    .swagger-ui .opblock-description-wrapper p { color: #888; }
    .swagger-ui .opblock.opblock-post   { border-color: #1a3a1a; background: #0d1a0d; }
    .swagger-ui .opblock.opblock-post   .opblock-summary { background: #0d1a0d; border-color: #1a3a1a; }
    .swagger-ui .opblock.opblock-get    { border-color: #0d1f3a; background: #0a1525; }
    .swagger-ui .opblock.opblock-get    .opblock-summary { background: #0a1525; border-color: #0d1f3a; }
    .swagger-ui .opblock.opblock-put    { border-color: #3a2a0a; background: #1f1800; }
    .swagger-ui .opblock.opblock-put    .opblock-summary { background: #1f1800; border-color: #3a2a0a; }
    .swagger-ui .opblock.opblock-delete { border-color: #3a0d0d; background: #200a0a; }
    .swagger-ui .opblock.opblock-delete .opblock-summary { background: #200a0a; border-color: #3a0d0d; }
    .swagger-ui .opblock-summary-method { border-radius: 4px; font-size: 12px; min-width: 60px; font-weight: 600; letter-spacing: 0.05em; }
    .swagger-ui .opblock.opblock-post   .opblock-summary-method { background: #22c55e; }
    .swagger-ui .opblock.opblock-get    .opblock-summary-method { background: #3b82f6; }
    .swagger-ui .opblock.opblock-put    .opblock-summary-method { background: #f59e0b; color: #000; }
    .swagger-ui .opblock.opblock-delete .opblock-summary-method { background: #ef4444; }
    .swagger-ui .opblock-tag { color: #f0ece0; font-size: 18px; border-bottom: 1px solid #1f1f1f; }
    .swagger-ui .opblock-tag:hover { background: #111; }
    .swagger-ui .opblock-tag small { color: #666; }
    .swagger-ui input[type=text], .swagger-ui input[type=password], .swagger-ui textarea, .swagger-ui select { background: #1a1a1a; border: 1px solid #2a2a2a; color: #d4d0c8; border-radius: 4px; }
    .swagger-ui input[type=text]:focus, .swagger-ui textarea:focus { border-color: #e8834a; outline: none; }
    .swagger-ui .btn { border-radius: 4px; font-weight: 500; }
    .swagger-ui .btn.execute { background: #e8834a; border-color: #e8834a; color: #000; }
    .swagger-ui .btn.execute:hover { background: #d4722f; border-color: #d4722f; }
    .swagger-ui .btn.cancel { background: transparent; border-color: #444; color: #888; }
    .swagger-ui .btn.try-out__btn { background: transparent; border: 1px solid #e8834a; color: #e8834a; }
    .swagger-ui .responses-inner { background: #0d0d0d; }
    .swagger-ui .response-col_status { color: #d4d0c8; }
    .swagger-ui table thead tr td, .swagger-ui table thead tr th { color: #888; border-bottom: 1px solid #1f1f1f; font-size: 12px; }
    .swagger-ui table tbody tr td { color: #d4d0c8; border-bottom: 1px solid #141414; }
    .swagger-ui .highlight-code { background: #111; }
    .swagger-ui .highlight-code code { color: #d4d0c8; }
    .swagger-ui .model-box { background: #111; border: 1px solid #1f1f1f; }
    .swagger-ui .model { color: #d4d0c8; }
    .swagger-ui .model-title { color: #e8834a; }
    .swagger-ui section.models { border: 1px solid #1f1f1f; background: #0d0d0d; }
    .swagger-ui section.models h4 { color: #f0ece0; }
    .swagger-ui .prop-type { color: #3b82f6; }
    .swagger-ui svg { fill: #888; }
    .swagger-ui .tab li { color: #888; }
    .swagger-ui .tab li.active { color: #e8834a; border-bottom: 2px solid #e8834a; }
    .swagger-ui .copy-to-clipboard { background: #1a1a1a; border: 1px solid #2a2a2a; }
    .swagger-ui .copy-to-clipboard button { background: transparent; }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0a0a0a; }
    ::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #3a3a3a; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.11.0/swagger-ui-bundle.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.11.0/swagger-ui-standalone-preset.min.js"></script>
  <script>
    window.onload = () => {
      SwaggerUIBundle({
        url: '/openapi.json',
        dom_id: '#swagger-ui',
        presets: [SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset],
        layout: 'StandaloneLayout',
        deepLinking: true,
        syntaxHighlight: { theme: 'monokai' },
      });
    };
  </script>
</body>
</html>
""")


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
    notes: Optional[str] = None

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
    return CustomerOut(**dict(row))


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
    return ItemOut(**dict(row))


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
    return OrderOut(**dict(row))


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