from sqlalchemy.orm import Session

from schemas.product_category import ProductCategoryDB

from models.product_category import (
    ProductCategoryCreate,
    ProductCategoryUpdate,
)


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
