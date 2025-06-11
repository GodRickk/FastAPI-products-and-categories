from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# from .database import Base
from database import Base


class ProductCategoryDB(Base):
    __tablename__ = "products_category"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String)

    products = relationship("ProductDB", back_populates="category")
