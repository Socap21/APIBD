from sqlalchemy.orm import Session
from models import Item, Customer, Order, Product, Supplier, Inventory, Shipment, Payment
from database import SessionLocal

def bulk_insert_data():
    db = SessionLocal()
    try:
        # Datos de ejemplo para la tabla Item
        items_data = [
            {"name": f"Item {i+1}", "description": f"Description for Item {i+1}"}
            for i in range(20)
        ]

        # Datos de ejemplo para la tabla Customer
        customers_data = [
            {"name": f"Customer {i+1}", "email": f"customer{i+1}@example.com"}
            for i in range(20)
        ]

        # Datos de ejemplo para la tabla Product
        products_data = [
            {"name": f"Product {i+1}", "price": round(10 + i * 2.5, 2)}
            for i in range(20)
        ]

        # Datos de ejemplo para la tabla Supplier
        suppliers_data = [
            {"name": f"Supplier {i+1}", "contact": f"contact{i+1}@supplier.com"}
            for i in range(20)
        ]

        # Datos de ejemplo para la tabla Inventory
        inventory_data = [
            {"product_id": i + 1, "stock": 50 + i * 5}
            for i in range(20)
        ]

        # Datos de ejemplo para la tabla Order
        orders_data = [
            {"customer_id": (i % 20) + 1, "total_price": round(100 + i * 10, 2)}
            for i in range(20)
        ]

        # Datos de ejemplo para la tabla Shipment
        shipments_data = [
            {"order_id": (i % 20) + 1, "tracking_number": f"TRACK{i+1000}"}
            for i in range(20)
        ]

        # Datos de ejemplo para la tabla Payment
        payments_data = [
            {"order_id": (i % 20) + 1, "payment_method": "Credit Card" if i % 2 == 0 else "PayPal", "payment_status": "Completed" if i % 3 != 0 else "Pending"}
            for i in range(20)
        ]

        # Inserción en bulk para cada tabla
        db.bulk_insert_mappings(Item, items_data)
        db.bulk_insert_mappings(Customer, customers_data)
        db.bulk_insert_mappings(Product, products_data)
        db.bulk_insert_mappings(Supplier, suppliers_data)
        db.bulk_insert_mappings(Inventory, inventory_data)
        db.bulk_insert_mappings(Order, orders_data)
        db.bulk_insert_mappings(Shipment, shipments_data)
        db.bulk_insert_mappings(Payment, payments_data)

        # Confirmar cambios en la base de datos
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error during bulk insert: {e}")
    finally:
        db.close()
