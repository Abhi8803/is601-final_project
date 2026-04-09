import sqlite3
import json


def init_db(json_path: str = "example_orders.json", db_path: str = "db.sqlite"):
    """
    Reads example_orders.json and initializes db.sqlite with:
      - customers   (id, name, phone)
      - items       (id, name, price)
      - orders      (id, customer_id FK, timestamp, notes)
      - order_items (id, order_id FK, item_id FK)

    Safe to re-run: drops and recreates all tables each time.
    """

    with open(json_path, "r") as f:
        raw_orders = json.load(f)

    con = sqlite3.connect(db_path)
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()

    # Drop existing tables (reverse dependency order)
    cur.execute("DROP TABLE IF EXISTS order_items")
    cur.execute("DROP TABLE IF EXISTS orders")
    cur.execute("DROP TABLE IF EXISTS customers")
    cur.execute("DROP TABLE IF EXISTS items")

    # Create tables
    cur.execute("""
        CREATE TABLE customers (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT    NOT NULL,
            phone TEXT    NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE items (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT    NOT NULL,
            price REAL    NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE orders (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL REFERENCES customers(id),
            timestamp   INTEGER,
            notes       TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE order_items (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL REFERENCES orders(id),
            item_id  INTEGER NOT NULL REFERENCES items(id)
        )
    """)

    # Seed data
    customer_map = {}  # (name, phone) -> customer_id
    item_map = {}      # (name, price) -> item_id
    order_count = 0

    for raw in raw_orders:
        # --- customer ---
        cust_key = (raw["name"], raw["phone"])
        if cust_key not in customer_map:
            cur.execute(
                "INSERT INTO customers (name, phone) VALUES (?, ?)",
                cust_key,
            )
            customer_map[cust_key] = cur.lastrowid

        customer_id = customer_map[cust_key]

        # --- order ---
        cur.execute(
            "INSERT INTO orders (customer_id, timestamp, notes) VALUES (?, ?, ?)",
            (customer_id, raw.get("timestamp"), raw.get("notes", "")),
        )
        order_id = cur.lastrowid
        order_count += 1

        # --- items + order_items ---
        for item in raw["items"]:
            item_key = (item["name"], item["price"])
            if item_key not in item_map:
                cur.execute(
                    "INSERT INTO items (name, price) VALUES (?, ?)",
                    item_key,
                )
                item_map[item_key] = cur.lastrowid

            item_id = item_map[item_key]

            cur.execute(
                "INSERT INTO order_items (order_id, item_id) VALUES (?, ?)",
                (order_id, item_id),
            )

    con.commit()
    con.close()

    print(f"Database initialized at '{db_path}'")
    print(f"  Customers   : {len(customer_map)}")
    print(f"  Items       : {len(item_map)}")
    print(f"  Orders      : {order_count}")


if __name__ == "__main__":
    init_db()
