from sqlalchemy.orm import Session

from schemas.product import ProductDB
from schemas.product_category import ProductCategoryDB

from models.product import Product, ProductCreate, ProductUpdate
from models.product_category import (
    ProductCategory,
    ProductCategoryCreate,
    ProductCategoryUpdate,
)


# TODO УДАЛИТЬ ЭТО туду по заверщению: ниже местами перепутаны файлы откуда идет информация о моделях и схемах
# (models -> schemas)
# (schemas -> models)


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductDB).offset(skip).limit(limit).all()


def get_products_with_filters(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_price: int = None,
    max_price: int = None,
    min_amount: int = None,
    max_amount: int = None,
    category_id: int = None,
):
    query = db.query(ProductDB)

    if min_price is not None:
        query = query.filter(ProductDB.price >= min_price)
    if max_price is not None:
        query = query.filter(ProductDB.price <= max_price)
    if min_amount is not None:
        query = query.filter(ProductDB.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(ProductDB.amount <= max_amount)
    if category_id is not None:
        query = query.filter(ProductDB.category_id == category_id)

    return query.offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int):
    return db.query(ProductDB).filter(ProductDB.id == product_id).first()


def get_product_by_name(db: Session, product_name: str):
    return db.query(ProductDB).filter(ProductDB.name == product_name).first()


def create_product(db: Session, product: ProductCreate):
    db_product = ProductDB(
        name=product.name, amount=product.amount, price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def create_product_with_category(db: Session, product: ProductCreate):
    db_product = ProductDB(
        name=product.name,
        amount=product.amount,
        price=product.price,
        category_id=product.category_id,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if db_product is None:
        return None

    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductCategoryDB).offset(skip).limit(limit).all()


def get_category(db: Session, category_id: int):
    return (
        db.query(ProductCategoryDB).filter(ProductCategoryDB.id == category_id).first()
    )


def get_category_by_name(db: Session, category_name: str):
    return (
        db.query(ProductCategoryDB)
        .filter(ProductCategoryDB.name == category_name)
        .first()
    )


def create_category(db: Session, category: ProductCategoryCreate):
    db_category = ProductCategoryDB(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int, category: ProductCategoryUpdate):
    db_category = (
        db.query(ProductCategoryDB).filter(ProductCategoryDB.id == category_id).first()
    )
    if db_category is None:
        return None

    update_data = category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = (
        db.query(ProductCategoryDB).filter(ProductCategoryDB.id == category_id).first()
    )
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category
