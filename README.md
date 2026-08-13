# JewelHub – Jewellery Marketplace

## 1. Project Overview

JewelHub is a jewellery marketplace application where multiple sellers can list jewellery products.

The application uses:

- React for the frontend
- FastAPI for the backend
- CognoDB as the graph database
- Neo4j official Python driver for database communication

The system stores relationships between sellers, products, categories, materials and purity.

---

## 2. Use Case

JewelHub allows jewellery sellers to add their products and allows users to view available jewellery.

Each seller can have multiple products.

Products are connected to:

- Seller
- Category
- Material
- Purity

Example:

Seller → Sells → Product → Belongs To → Category

This relationship-based structure allows the application to efficiently explore connections between sellers and their products.

---

## 3. Why Graph Database?

A graph database is suitable for JewelHub because the application contains many relationships.

The main relationships are:

Seller → Product  
Product → Category  
Product → Material  
Product → Purity

For example, the application can find all products sold by a particular seller and also retrieve the category of each product through a multi-hop graph traversal.

This can be naturally represented as:

Seller
  |
SELLS
  |
Product
  |
BELONGS_TO
  |
Category

The graph model makes relationship-based queries straightforward and readable.

---

## 4. Data Model

### Nodes

- Seller
- Product
- Category
- Material
- Purity

### Relationships

- Seller -[:SELLS]-> Product
- Product -[:BELONGS_TO]-> Category
- Product -[:MADE_OF]-> Material
- Product -[:HAS_PURITY]-> Purity

### Example

Seller: Vinay Jewellers
        |
      SELLS
        |
   Gold Ring
        |
   BELONGS_TO
        |
      Rings

---

## 5. Technology Stack

### Frontend
- React
- JavaScript
- CSS

### Backend
- Python
- FastAPI
- Uvicorn

### Database
- CognoDB
- Neo4j Python Driver

### Configuration
- python-dotenv
- Environment variables

---

## 6. Project Structure

```text
jewelhub/
│
├── backend/
│   ├── main.py
│   ├── seed.py
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── README.md
└── .gitignore