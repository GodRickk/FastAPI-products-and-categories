from pydantic import BaseModel

class ProductBase(BaseModel):
    price: int
    amount: int
    name: str
    

class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    category_id: int | None

    class Config:
        orm_mode = True



class ProductCategoryBase(BaseModel):
    name: str


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategory(ProductCategoryBase):
    id: int
    products: list[Product] = []

    class Config:
        orm_mode = True
