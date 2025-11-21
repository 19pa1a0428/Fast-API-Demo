from fastapi import FastAPI, Depends 
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# app.add_middleWare(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"]
# )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    return db_products


@app.get("/products/{id}")

def get_produc_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product 
    return "Product not found"

@app.post("/products")

def add_product(product : Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()

@app.put("/products/{id}")

def update_product(id: int, product : Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product added"
    else:
        return "No product found"
@app.delete("/products/{id}")

def delete_Product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted"
    else:
        return "Product not found"
