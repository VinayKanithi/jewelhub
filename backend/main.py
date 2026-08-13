import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from neo4j import GraphDatabase
from pydantic import BaseModel


load_dotenv()

COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")


driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USERNAME, COGNODB_PASSWORD)
)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to JewelHub API"
    }


@app.get("/products")
def get_products():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (p:Product)
            RETURN p.name AS name,
                   p.material AS material,
                   p.purity AS purity,
                   p.weight AS weight,
                   p.price AS price,
                   p.category AS category
            """
        )

        products = [record.data() for record in result]

    return products


class Product(BaseModel):
    seller_id: str
    name: str
    material: str
    purity: str
    weight:float
    price: float
    category: str

class Seller(BaseModel):
    name: str
    email: str
    phone: str
    business_name: str

@app.post("/sellers")
def add_seller(seller: Seller):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (existing:Seller)
            WITH count(existing) AS seller_count

            CREATE (s:Seller {
                seller_id: 'SEL' + toString(seller_count + 1),
                name: $name,
                email: $email,
                phone: $phone,
                business_name: $business_name
            })

            RETURN s.seller_id AS seller_id,
                   s.name AS name,
                   s.email AS email,
                   s.phone AS phone,
                   s.business_name AS business_name
            """,
            name=seller.name,
            email=seller.email,
            phone=seller.phone,
            business_name=seller.business_name
        )

        return result.single().data()

@app.get("/sellers")
def get_sellers():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (s:Seller)
            RETURN s.seller_id AS seller_id,
                   s.name AS name,
                   s.email AS email,
                   s.phone AS phone,
                   s.business_name AS business_name
            LIMIT 20
            """
        )

        sellers = [record.data() for record in result]

    return sellers
    
@app.post("/products")
def add_product(product: Product):
    with driver.session() as session:
        session.run(
          """
            MATCH (s:Seller)
            WHERE s.seller_id = $seller_id
            CREATE (p:Product {
                name: $name,
                material: $material,
                purity: $purity,
                weight: $weight,
                price: $price
            })

            MERGE (c:Category {name: $category})
            MERGE (m:Material {name: $material})
            MERGE (pu:Purity {name: $purity})

            MERGE (s)-[:SELLS]->(p)
            MERGE (p)-[:BELONGS_TO]->(c)
            MERGE (p)-[:MADE_OF]->(m)
            MERGE (p)-[:HAS_PURITY]->(pu)
            """,
            seller_id=product.seller_id,
            name=product.name,
            material=product.material,
            purity=product.purity,
            weight=product.weight,
            price=product.price,
            category=product.category
        )

    return {
        "message": "Product added successfully",
        "product": product
    }


# NEW THING
@app.get("/seller/{seller_id}/products")
def get_seller_products(seller_id: str):
    try:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (s:Seller {seller_id: $seller_id})-[:SELLS]->(p:Product)
                      -[:BELONGS_TO]->(c:Category)
                RETURN s.seller_id AS seller_id,
                       s.business_name AS business_name,
                       p.name AS product,
                       p.price AS price,
                       c.name AS category
                LIMIT 20
                """,
                seller_id=seller_id
            )

            return [record.data() for record in result]

    except Exception as e:
        return {
            "error": "Unable to retrieve seller products"
        }