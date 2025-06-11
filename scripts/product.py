from sqlalchemy.orm import Session

from schemas.product import ProductDB

from models.product import ProductCreate, ProductUpdate


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
