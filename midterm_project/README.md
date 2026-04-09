# IS601 Midterm Project – Dosa Order Processing

## Project Description

For this midterm project, I created a Python script that processes restaurant order data stored in a JSON file. The goal of the program is to analyze the orders and generate two summary files that help the restaurant better organize its customer information and track menu item popularity.

The program reads an orders file and produces:

* **customers.json** – a dictionary mapping phone numbers to customer names
* **items.json** – a dictionary containing menu items, their price, and how many times each item was ordered

---

## How the Program Works

1. The program reads a JSON file containing restaurant orders.
2. It extracts the customer phone numbers and names.
3. It counts how many times each menu item appears in the orders.
4. It generates two new JSON files summarizing the data.

This allows the restaurant owner to easily see who their customers are and which items are ordered the most.

---

## Input File

The input file is a JSON file that contains a list of orders. Each order includes:

* Customer name
* Phone number
* A list of items ordered

Example:

```json id="puzj35"
{
  "name": "Karl",
  "phone": "609-555-0124",
  "items": [
    {
      "name": "Butter Masala Dosa",
      "price": 12.95
    }
  ]
}
```

---

## Output Files

### customers.json

This file contains phone numbers as keys and customer names as values.

Example:

```json id="whprbi"
{
  "609-555-0124": "Karl",
  "732-555-1234": "Mike"
}
```

---

### items.json

This file contains menu items as keys and an object showing the price and number of times that item was ordered.

Example:

```json id="q37q92"
{
  "Butter Masala Dosa": {
    "price": 12.95,
    "orders": 52
  }
}
```

---

## How to Run the Program

Navigate to the project folder and run the script using Python.

```bash id="8u3aau"
python3 process_orders.py example_orders.json
```

After running the program, the following files will be created:

* `customers.json`
* `items.json`

---

## Design Approach

I organized the program using separate functions to keep the code clean and easier to understand. These functions handle loading the data, extracting customers, counting menu items, and saving the results as JSON files.

I also used Python dictionaries and `defaultdict` to efficiently count how many times each menu item appears in the orders.

---

## Technologies Used

* Python 3
* JSON
* Git and GitHub

---
Abhiram Panuganti (ap3364)
ap3364@njit.edu
