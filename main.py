from fastapi import FastAPI 
from models import Product

app = FastAPI()


products = [
    Product(id = 1, name = "Mobile", description = "Iphone", price = 999, quantity = 10),
    Product(id = 2, name = "phone", description = "Android", price = 899, quantity = 20),
    Product(id = 3, name = "Car", description = "Cars", price = 999, quantity = 10),
    Product(id = 5, name = "Bike", description = "Bike", price = 899, quantity = 20)
]

@app.get("/products")


def get_all_products():
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
