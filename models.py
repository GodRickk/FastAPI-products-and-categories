from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    category_id = Column(Integer, ForeignKey("product_ctegory.id"))

    price = Column(Integer)
    amount = Column(Integer)
    name = Column(String, unique=True)

    category = relationship("ProductCategory", back_populates="products")


class ProductCategory(Base):
    __tablename__ = "products_category"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String, unique=True)

    products = relationship("Product", back_populates="category")


