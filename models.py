from sqlalchemy import Column,Integer,String,Float,Text,ForeignKey
from database import Base
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(150),nullable=False)
    price = Column(Float,nullable=False)
    discount_price = Column(Float)
    quantity = Column(Integer,default=0)
    image = Column(String(255))
    category_id = Column(Integer,ForeignKey("categories.id"))
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),unique=True,nullable=False)
    description = Column(Text)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    email = Column(String(150),unique=True,nullable=False)
    password = Column(String(255),nullable=False)