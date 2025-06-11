from typing import Optional
from pydantic import BaseModel

from models.product import Product


class ProductCategoryBase(BaseModel):
    name: str


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(BaseModel):
    name: Optional[str] = None


class ProductCategory(ProductCategoryBase):
    id: int
    products: list[Product] = []

    class Config:
        orm_mode = True
