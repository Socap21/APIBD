from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import union_all
from sqlalchemy.sql import text
from typing import List
import models, schemas
from database import engine, get_db
from faker import Faker

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI()

# Fake data generator
fake = Faker()

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
    
    for _ in range(10):  # Generar 10 registros de ejemplo
        customer = models.Customer(
            name=fake.name(),        # Genera un nombre aleatorio
            email=fake.email()       # Genera un email aleatorio
        )
        db.add(customer)

    for _ in range(10):  # Generar 10 registros de ejemplo
        inventory_item = models.Inventory(
            product_id=fake.random_int(min=1, max=100),  # Genera un ID de producto aleatorio entre 1 y 100
            stock=fake.random_int(min=0, max=500)        # Genera una cantidad de stock aleatoria entre 0 y 500
        )
        db.add(inventory_item)

    for _ in range(10):  # Generar 10 registros de ejemplo
        product = models.Products(
            name=fake.word().capitalize(),          # Genera un nombre de producto aleatorio
            price=round(fake.random_number(digits=4) / 100, 2)  # Genera un precio aleatorio con dos decimales
        )
        db.add(product)

    for _ in range(10):  # Generar 10 registros de ejemplo
        order = models.Orders(
            customer_id=fake.random_int(min=1, max=100),   # Genera un ID de cliente aleatorio entre 1 y 100
            total_price=round(fake.random_number(digits=5) / 100, 2)  # Genera un precio total aleatorio con dos decimales
        )
        db.add(order)

    for _ in range(10):  # Generar 10 registros de ejemplo
        payment = models.Payments(
            order_id=fake.random_int(min=1, max=100),  # Genera un ID de pedido aleatorio entre 1 y 100
            payment_method=fake.random_element(elements=["Credit Card", "PayPal", "Bank Transfer", "Cash"]),  # Selecciona un método de pago aleatorio
            payment_status=fake.random_element(elements=["Completed", "Pending", "Failed", "Refunded"])  # Selecciona un estado de pago aleatorio
        )
        db.add(payment) 

    for _ in range(10):  # Generar 10 registros de ejemplo
        shipment = models.Shipment(
            order_id=fake.random_int(min=1, max=100),  # Genera un ID de pedido aleatorio entre 1 y 100
            tracking_number=fake.bothify(text='???-#####')  # Genera un número de seguimiento aleatorio, ej. "ABC-12345"
        )
        db.add(shipment)

    for _ in range(10):  # Generar 10 registros de ejemplo
        supplier = models.Supplier(
            name=fake.company(),  # Genera un nombre de empresa aleatorio
            contact=fake.name()   # Genera un nombre de contacto aleatorio
        )
        db.add(supplier)


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

@app.get("/orders_with_payments/", response_model=List[schemas.OrderWithPayment])
def get_orders_with_payments(db: Session = Depends(get_db)):
    query = text("""
        SELECT orders.id AS order_id, orders.customer_id, orders.total_price, 
               payments.payment_status, payments.payment_method
        FROM orders
        LEFT JOIN payments ON orders.id = payments.order_id
    """)
    result = db.execute(query).mappings().all()
    return result

@app.get("/orders_with_customers/", response_model=List[schemas.OrderWithCustomer])
def get_orders_with_customers(db: Session = Depends(get_db)):
    query = text("""
        SELECT orders.id AS order_id, customers.name AS customer_name, 
               customers.email AS customer_email, orders.total_price
        FROM orders
        INNER JOIN customers ON orders.customer_id = customers.id
    """)
    result = db.execute(query).mappings().all()
    return result

@app.get("/suppliers_with_inventory/", response_model=List[schemas.SupplierInventory])
def get_suppliers_with_inventory(db: Session = Depends(get_db)):
    query = text("""
        SELECT suppliers.name AS supplier_name, suppliers.contact AS supplier_contact, 
               inventory.product_id, inventory.stock
        FROM suppliers
        LEFT JOIN inventory ON suppliers.id = inventory.product_id
    """)
    result = db.execute(query).mappings().all()
    return result

@app.get("/shipments_with_orders/", response_model=List[schemas.ShipmentWithOrder])
def get_shipments_with_orders(db: Session = Depends(get_db)):
    query = text("""
        SELECT shipments.id AS shipment_id, shipments.tracking_number, 
               orders.id AS order_id, orders.total_price
        FROM shipments
        INNER JOIN orders ON shipments.order_id = orders.id
    """)
    result = db.execute(query).mappings().all()
    return result

@app.get("/customers_with_orders/", response_model=List[schemas.CustomerWithOrders])
def get_customers_with_orders(db: Session = Depends(get_db)):
    query = text("""
        SELECT customers.id AS customer_id, customers.name AS customer_name, customers.email AS customer_email,
               orders.id AS order_id, orders.total_price
        FROM customers
        LEFT JOIN orders ON customers.id = orders.customer_id
    """)
    result = db.execute(query).mappings().all()
    return result

@app.get("/suppliers_with_products/", response_model=List[schemas.SupplierWithProducts])
def get_suppliers_with_products(db: Session = Depends(get_db)):
    query = text("""
        SELECT suppliers.id AS supplier_id, suppliers.name AS supplier_name,
               products.name AS product_name, products.price
        FROM suppliers
        LEFT JOIN products ON suppliers.id = products.id
    """)
    result = db.execute(query).mappings().all()
    return result

@app.get("/completed_payments/", response_model=List[schemas.CompletedPayments])
def get_completed_payments(db: Session = Depends(get_db)):
    query = text("""
        SELECT payments.id AS payment_id, payments.order_id, payments.payment_method, 
               orders.total_price
        FROM payments
        INNER JOIN orders ON payments.order_id = orders.id
        WHERE payments.payment_status = 'completed'
    """)
    result = db.execute(query).mappings().all()
    return result

@app.get("/orders_with_shipments/", response_model=List[schemas.OrderWithShipment])
def get_orders_with_shipments(db: Session = Depends(get_db)):
    query = text("""
        SELECT orders.id AS order_id, orders.total_price,
               shipments.tracking_number
        FROM orders
        LEFT JOIN shipments ON orders.id = shipments.order_id
    """)
    result = db.execute(query).mappings().all()
    return result

@app.get("/payments_with_shipments/", response_model=List[schemas.PaymentWithShipment])
def get_payments_with_shipments(db: Session = Depends(get_db)):
    query = text("""
        SELECT payments.id AS payment_id, payments.order_id, payments.payment_method,
               shipments.tracking_number
        FROM payments
        LEFT JOIN shipments ON payments.order_id = shipments.order_id
    """)
    result = db.execute(query).mappings().all()
    return result

@app.get("/products_with_inventory_status/", response_model=List[schemas.ProductInventoryStatus])
def get_products_with_inventory_status(db: Session = Depends(get_db)):
    # Realizar el LEFT JOIN entre Products e Inventory
    left_join_query = (
        db.query(
            models.Products.id.label("product_id"),
            models.Products.name.label("product_name"),
            models.Products.price.label("price"),
            models.Inventory.stock.label("stock")
        )
        .outerjoin(models.Inventory, models.Products.id == models.Inventory.product_id)
    )
    
    # Realizar el RIGHT JOIN entre Inventory y Products
    right_join_query = (
        db.query(
            models.Inventory.product_id.label("product_id"),
            models.Products.name.label("product_name"),
            models.Products.price.label("price"),
            models.Inventory.stock.label("stock")
        )
        .outerjoin(models.Products, models.Inventory.product_id == models.Products.id)
    )
    
    # Unir ambas consultas con union_all para simular FULL OUTER JOIN
    full_outer_join_query = left_join_query.union_all(right_join_query)
    
    # Ejecutar la consulta y devolver resultados
    result = db.execute(full_outer_join_query).mappings().all()
    return result

@app.get("/orders_with_payment_status/", response_model=List[schemas.OrderWithPaymentStatus])
def get_orders_with_payment_status(db: Session = Depends(get_db)):
    query = text("""
        SELECT orders.id AS order_id, orders.total_price,
               payments.payment_status
        FROM orders
        LEFT JOIN payments ON orders.id = payments.order_id
    """)
    result = db.execute(query).mappings().all()
    return result

@app.get("/inventory_with_suppliers/", response_model=List[schemas.InventoryWithSupplier])
def get_inventory_with_suppliers(db: Session = Depends(get_db)):
    query = text("""
        SELECT inventory.id AS inventory_id, inventory.stock, inventory.product_id,
               suppliers.name AS supplier_name, suppliers.contact
        FROM inventory
        INNER JOIN suppliers ON inventory.product_id = suppliers.id
    """)
    result = db.execute(query).mappings().all()
    return result

# -------------------- Root endpoint --------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to the  API!"}


    