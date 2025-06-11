from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# from .database import Base
from database import Base


class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    category_id = Column(Integer, ForeignKey("products_category.id"))

    price = Column(Integer)
    amount = Column(Integer)
    name = Column(String, unique=True)

    category = relationship("ProductCategoryDB", back_populates="products")
