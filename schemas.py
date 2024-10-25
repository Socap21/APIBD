from pydantic import BaseModel
from typing import Optional

# ------------------- Esquema para la tabla "Item" -------------------
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True

# ------------------- Esquema para la tabla "Customer" -------------------
class CustomerBase(BaseModel):
    name: str
    email: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True

# ------------------- Esquema para la tabla "Order" -------------------
class OrderBase(BaseModel):
    customer_id: int
    total_price: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True

# ------------------- Esquema para la tabla "Product" -------------------
class ProductBase(BaseModel):
    name: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

# ------------------- Esquema para la tabla "Supplier" -------------------
class SupplierBase(BaseModel):
    name: str
    contact: str

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int

    class Config:
        orm_mode = True

# ------------------- Esquema para la tabla "Inventory" -------------------
class InventoryBase(BaseModel):
    product_id: int
    stock: int

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int

    class Config:
        orm_mode = True

# ------------------- Esquema para la tabla "Shipment" -------------------
class ShipmentBase(BaseModel):
    order_id: int
    tracking_number: str

class ShipmentCreate(ShipmentBase):
    pass

class Shipment(ShipmentBase):
    id: int

    class Config:
        orm_mode = True

# ------------------- Esquema para la tabla "Payment" -------------------
class PaymentBase(BaseModel):
    order_id: int
    payment_method: str
    payment_status: str

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int

    class Config:
        orm_mode = True


