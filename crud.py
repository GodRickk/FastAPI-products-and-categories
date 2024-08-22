from sqlalchemy.orm import Session

# from . import models, schemas
import models, schemas

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_product_by_name(db: Session, product_name: str):
    return db.query(models.Product).filter(models.Product.name == product_name).first()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, amount=product.amount, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def create_product_with_category(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, amount=product.amount, price=product.price, category_id=product.category_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProductCategory).offset(skip).limit(limit).all()


def get_category(db: Session, category_id: int):
    return db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id).first()


def get_category_by_name(db: Session, category_name: str):
    return db.query(models.ProductCategory).filter(models.ProductCategory.name == category_name).first()


def create_category(db: Session, category: schemas.ProductCategoryCreate):
    db_category = models.ProductCategory(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
