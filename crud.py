from sqlalchemy.orm import Session
import models, schemas


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_products_with_filters(db: Session, skip: int = 0, limit: int = 100,
                              min_price: int = None, max_price: int = None,
                              min_amount: int = None, max_amount: int = None, 
                              category_id: int = None):
    query = db.query(models.Product)

    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    if min_amount is not None:
        query = query.filter(models.Product.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(models.Product.amount <= max_amount)
    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)
    
    return query.offset(skip).limit(limit).all()

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


def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        return None

    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product    


def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
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


def update_category(db: Session, category_id: int, category: schemas.ProductCategoryUpdate):
    db_category = db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id).first()
    if db_category is None:
        return None
    
    update_data = category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category
