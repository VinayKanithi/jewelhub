# import os

# from dotenv import load_dotenv
# from neo4j import GraphDatabase

# load_dotenv()

# URI = os.getenv("COGNODB_URI")
# USERNAME = os.getenv("COGNODB_USERNAME")
# PASSWORD = os.getenv("COGNODB_PASSWORD")

# driver = GraphDatabase.driver(
#     URI,
#     auth=(USERNAME, PASSWORD)
# )


# products = [
#     {
#         "name": "Ring",
#         "material": "Gold",
#         "purity": "22K",
#         "price": 45000,
#         "category": "Rings"
#     },
#     {
#         "name": "Necklace",
#         "material": "Gold",
#         "purity": "22K",
#         "price": 85000,
#         "category": "Necklaces"
#     },
#     {
#         "name": "Earrings",
#         "material": "Gold",
#         "purity": "Diamond",
#         "price": 60000,
#         "category": "Earrings"
#     }
# ]


# with driver.session() as session:
#     for product in products:
#         session.run(
#             """
#              MERGE (s:Seller {name: "Royal Jewellers"})

#             MERGE (p:Product {name: $name})
#             SET p.material = $material,
#                 p.purity = $purity,
#                 p.price = $price

#             MERGE (c:Category {name: $category})
#             MERGE (m:Material {name: $material})
#             MERGE (pu:Purity {name: $purity})

#             MERGE (s)-[:SELLS]->(p)
#             MERGE (p)-[:BELONGS_TO]->(c)
#             MERGE (p)-[:MADE_OF]->(m)
#             MERGE (p)-[:HAS_PURITY]->(pu)
#             """,
#             **product
#         )

# print("Products added successfully!")

# driver.close()

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")

driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USERNAME, COGNODB_PASSWORD)
)

products = [
    {
        "name": "Gold Ring",
        "material": "Gold",
        "purity": "22K",
        "weight": 5.5,
        "price": 45000,
        "category": "Rings"
    },
    {
        "name": "Gold Necklace",
        "material": "Gold",
        "purity": "22K",
        "weight": 15.2,
        "price": 85000,
        "category": "Necklaces"
    },
    {
        "name": "Diamond Earrings",
        "material": "Gold",
        "purity": "18K",
        "weight": 4.2,
        "price": 60000,
        "category": "Earrings"
    },
    {
        "name": "Gold Bracelet",
        "material": "Gold",
        "purity": "22K",
        "weight": 8.5,
        "price": 55000,
        "category": "Bracelets"
    }
]

with driver.session() as session:

    # Create sellers
    session.run("""
        MERGE (s:Seller {seller_id: "SEL1"})
        SET s.name = "Royal Jewellers",
            s.email = "royal@example.com",
            s.phone = "9000000001",
            s.business_name = "Royal Jewellers"
    """)

    session.run("""
        MERGE (s:Seller {seller_id: "SEL2"})
        SET s.name = "Vinay",
            s.email = "vinay@example.com",
            s.phone = "9876543210",
            s.business_name = "Vinay Jewellers"
    """)

    session.run("""
        MERGE (s:Seller {seller_id: "SEL3"})
        SET s.name = "Ravi",
            s.email = "ravi@example.com",
            s.phone = "9123456789",
            s.business_name = "Ravi Jewellers"
    """)

    # Add products
    for product in products:
        session.run("""
            MATCH (s:Seller {seller_id: "SEL2"})

            MERGE (p:Product {name: $name})
            SET p.material = $material,
                p.purity = $purity,
                p.weight = $weight,
                p.price = $price

            MERGE (c:Category {name: $category})
            MERGE (m:Material {name: $material})
            MERGE (pu:Purity {name: $purity})

            MERGE (s)-[:SELLS]->(p)
            MERGE (p)-[:BELONGS_TO]->(c)
            MERGE (p)-[:MADE_OF]->(m)
            MERGE (p)-[:HAS_PURITY]->(pu)
        """, **product)

print("Seed data inserted successfully!")

driver.close()