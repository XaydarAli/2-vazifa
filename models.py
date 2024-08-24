from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime,Text,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone_number = Column(String(50))
    password = Column(Text, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    email = Column(String, unique=True, nullable=False)
    orders = relationship('Order', back_populates='user')

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    orders = relationship('OrderProduct', back_populates='product')

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price})"

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='orders')
    products = relationship('OrderProduct', back_populates='order')
    cargo = relationship('Cargo', uselist=False, back_populates='order')

    def __repr__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, created_at={self.created_at})"

class OrderProduct(Base):
    __tablename__ = 'order_products'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    order = relationship('Order', back_populates='products')
    product = relationship('Product', back_populates='orders')

    def __repr__(self):
        return f"OrderProduct(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})"

class Cargo(Base):
    __tablename__ = 'cargos'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    shipping_address = Column(String, nullable=False)
    tracking_number = Column(String, unique=True, nullable=True)
    order = relationship('Order', back_populates='cargo')

    def __repr__(self):
        return f"Cargo(id={self.id}, order_id={self.order_id}, shipping_address={self.shipping_address}, tracking_number={self.tracking_number})"
