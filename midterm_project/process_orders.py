import json
import argparse
import re
from collections import defaultdict

# Phone number format: xxx-xxx-xxxx
PHONE_PATTERN = re.compile(r"^\d{3}-\d{3}-\d{4}$")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Process restaurant orders.")
    parser.add_argument("input_file", help="JSON file containing orders")
    return parser.parse_args()


def load_orders(filename):
    """Load orders from a JSON file."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        exit(1)


def build_customers(orders):
    """Create dictionary of phone numbers -> customer names."""
    customers = {}

    for order in orders:
        phone = order.get("phone")
        name = order.get("name")

        if phone and name and PHONE_PATTERN.match(phone):
            customers[phone] = name

    return customers


def build_items(orders):
    """Create dictionary of items with price and number of orders."""
    items = defaultdict(lambda: {"price": 0.0, "orders": 0})

    for order in orders:
        for item in order.get("items", []):
            item_name = item.get("name")
            price = item.get("price", 0)

            if item_name:
                items[item_name]["price"] = price
                items[item_name]["orders"] += 1

    return dict(items)


def write_json(filename, data):
    """Write dictionary data to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def main():
    """Main program execution."""
    args = parse_args()

    orders = load_orders(args.input_file)

    customers = build_customers(orders)
    items = build_items(orders)

    write_json("customers.json", customers)
    write_json("items.json", items)

    print(f"Processed {len(orders)} orders successfully.")
    print(f"Generated {len(customers)} customers.")
    print(f"Generated {len(items)} items.")


if __name__ == "__main__":
    main()
