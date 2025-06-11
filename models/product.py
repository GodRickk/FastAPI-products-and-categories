from typing import Optional
from pydantic import BaseModel


class ProductBase(BaseModel):
    price: int
    amount: int
    name: str
    category_id: None | int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    amount: Optional[int] = None
    category_id: Optional[int] = None


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
