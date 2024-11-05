from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.sql import text
from typing import List
import models, schemas
from database import engine, get_db
from faker import Faker
from bulk_insert import bulk_insert_data

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI()

# Fake data generator
fake = Faker()

@app.on_event("startup")
def startup_event():
    bulk_insert_data()
# -------------------- CRUD Endpoints --------------------

# Create (POST) Item
@app.post("/items/", response_model=List[schemas.Item])
def create_items(items: List[schemas.ItemCreate], db: Session = Depends(get_db)):
    db_items = [models.Item(**item.dict()) for item in items]
    db.bulk_save_objects(db_items)
    db.commit()
    return db_items

# Read (GET) all items
@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items

# Read (GET) a single item by ID
@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Update (PUT) an item by ID
@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

# Delete (DELETE) an item by ID
@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return db_item

# -------------------- Endpoint to generate synthetic data --------------------

@app.post("/generate_data/")
def generate_synthetic_data(db: Session = Depends(get_db)):
    # Generar datos sintéticos para las tablas
    for _ in range(10):  # Generar 10 registros de ejemplo
        item = models.Item(name=fake.word(), description=fake.sentence())
        db.add(item)

    # Repetir para otras tablas...

    db.commit()
    return {"message": "Datos sintéticos generados con éxito"}

# -------------------- Endpoint to get products with inventory --------------------

@app.get("/products_with_inventory/", response_model=List[schemas.ProductWithInventory])
def get_products_with_inventory(db: Session = Depends(get_db)):
    # Definir la consulta usando un SQL explícito o usando ORM
    result = db.execute(text("""
        SELECT products.id AS product_id, products.name AS product_name, products.price, inventory.stock 
        FROM products 
        INNER JOIN inventory ON products.id = inventory.product_id;
    """)).mappings().all()  # Usa .mappings() para obtener un diccionario por cada fila
    
    # Convertir el resultado en una lista de diccionarios
    products_with_inventory = [
        {
            "product_id": row["product_id"],
            "product_name": row["product_name"],
            "price": row["price"],
            "stock": row["stock"]
        }
        for row in result
    ]
    
    return products_with_inventory

# -------------------- Root endpoint --------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to the  API!"}


    