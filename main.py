from fastapi import FastAPI, Depends 
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")

def greet():
    return "Hello"

products = [
    Product(id = 1, name = "Mobile", description = "Iphone", price = 999, quantity = 10),
    Product(id = 2, name = "phone", description = "Android", price = 899, quantity = 20),
    Product(id = 3, name = "Car", description = "Cars", price = 999, quantity = 10),
    Product(id = 5, name = "Bike", description = "Bike", price = 899, quantity = 20)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()

    count = db.query(database_models.Product).count

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()

@app.get("/products")


def get_all_products(db: Session = Depends(get_db)):

    db_products = db.query(database_models.Product).all()

    return products


@app.get("/product/{id}")

def get_produc_by_id(id: int):
    for product in products:
        if product.id == id:
            return product 
    return "Product not found"

@app.post("/product")

def add_product(product : Product):
    products.append(product)
    return product

@app.put("/product")

def update_product(id: int, product : Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product added successfully"
    return "Product not found"

@app.delete("/product")

def delete_Product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "Porduct deleted"
    return "Product not found"
