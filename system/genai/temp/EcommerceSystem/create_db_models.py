# using resolved_model gpt-4o-2024-08-06# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import date   
from datetime import datetime

logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


class Customer(Base):
    """description: Customers table, storing customer details and account balances."""
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    balance = Column(Integer)  # Derived column
    credit_limit = Column(Integer, default=1000)



class Order(Base):
    """description: Orders table, each linked to a customer."""
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    date_shipped = Column(DateTime)
    amount_total = Column(Integer)  # Derived column
    notes = Column(String)



class Item(Base):
    """description: Items table, each linked to an order and a product."""
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, default=1)
    unit_price = Column(Integer)  # Copied from product
    amount = Column(Integer)  # Derived column



class Product(Base):
    """description: Products table, storing product details."""
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    unit_price = Column(Integer)



# ALS/GenAI: Create an SQLite database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ALS/GenAI: Prepare for sample data

from datetime import date

customer1 = Customer(id=1, name='John Doe', balance=200, credit_limit=1000)
customer2 = Customer(id=2, name='Jane Smith', balance=300, credit_limit=1500)
customer3 = Customer(id=3, name='Emily Davis', balance=150, credit_limit=800)
customer4 = Customer(id=4, name='Michael Brown', balance=50, credit_limit=1200)

order1 = Order(id=1, customer_id=1, date_shipped=date(2023, 1, 15), amount_total=150, notes='Urgent delivery')
order2 = Order(id=2, customer_id=2, date_shipped=None, amount_total=200, notes='Standard shipping')
order3 = Order(id=3, customer_id=3, date_shipped=date(2023, 2, 10), amount_total=100, notes='Gift package')
order4 = Order(id=4, customer_id=4, date_shipped=None, amount_total=50, notes='Fragile items')

product1 = Product(id=1, name='Widget', unit_price=50)
product2 = Product(id=2, name='Gadget', unit_price=75)
product3 = Product(id=3, name='Thing', unit_price=100)
product4 = Product(id=4, name='Device', unit_price=200)

item1 = Item(id=1, order_id=1, product_id=1, quantity=2, unit_price=50, amount=100)
item2 = Item(id=2, order_id=2, product_id=2, quantity=1, unit_price=75, amount=75)
item3 = Item(id=3, order_id=3, product_id=3, quantity=1, unit_price=100, amount=100)
item4 = Item(id=4, order_id=4, product_id=4, quantity=1, unit_price=200, amount=200)



session.add_all([customer1, customer2, customer3, customer4, order1, order2, order3, order4, product1, product2, product3, product4, item1, item2, item3, item4])
session.commit()
