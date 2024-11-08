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

# Esquema para el modelo de productos con inventario
class ProductWithInventory(BaseModel):
    product_id: int
    product_name: str
    price: float
    stock: int

    class Config:
        orm_mode = True
    
# Esquema para pedidos con pago opcional
class OrderWithPayment(BaseModel):
    order_id: int
    customer_id: int
    total_price: float
    payment_status: Optional[str] = None
    payment_method: Optional[str] = None

    class Config:
        orm_mode = True

# Esquema para pedidos con información del cliente
class OrderWithCustomer(BaseModel):
    order_id: int
    customer_name: str
    customer_email: str
    total_price: float

    class Config:
        orm_mode = True

# Esquema para proveedores con inventario opcional
class SupplierInventory(BaseModel):
    supplier_name: str
    supplier_contact: str
    product_id: Optional[int] = None
    stock: Optional[int] = None

    class Config:
        orm_mode = True

# Esquema para envíos con información del pedido
class ShipmentWithOrder(BaseModel):
    shipment_id: int
    tracking_number: str
    order_id: int
    total_price: float

    class Config:
        orm_mode = True

# Esquema para clientes con pedidos opcionales
class CustomerWithOrders(BaseModel):
    customer_id: int
    customer_name: str
    customer_email: str
    order_id: Optional[int] = None
    total_price: Optional[float] = None

    class Config:
        orm_mode = True

# Esquema para proveedores con productos opcionales
class SupplierWithProducts(BaseModel):
    supplier_id: int
    supplier_name: str
    product_name: Optional[str] = None
    price: Optional[float] = None

    class Config:
        orm_mode = True

# Esquema para pagos completados con total del pedido
class CompletedPayments(BaseModel):
    payment_id: int
    order_id: int
    payment_method: str
    total_price: float

    class Config:
        orm_mode = True

# Esquema para pedidos con envíos opcionales
class OrderWithShipment(BaseModel):
    order_id: int
    total_price: float
    tracking_number: Optional[str] = None

    class Config:
        orm_mode = True

# Esquema para pagos con detalles de envío opcionales
class PaymentWithShipment(BaseModel):
    payment_id: int
    order_id: int
    payment_method: str
    tracking_number: Optional[str] = None

    class Config:
        orm_mode = True

# Esquema para el resultado de FULL OUTER JOIN entre Products e Inventory
class ProductInventoryStatus(BaseModel):
    product_id: Optional[int]  # Puede ser nulo si no hay coincidencia en Inventory
    product_name: Optional[str]
    price: Optional[float]
    stock: Optional[int]

    class Config:
        orm_mode = True

# Esquema para pedidos con estado de pago opcional
class OrderWithPaymentStatus(BaseModel):
    order_id: int
    total_price: float
    payment_status: Optional[str] = None

    class Config:
        orm_mode = True

# Esquema para productos en inventario con información del proveedor
class InventoryWithSupplier(BaseModel):
    inventory_id: int
    stock: int
    product_id: int
    supplier_name: str
    contact: str

    class Config:
        orm_mode = True

