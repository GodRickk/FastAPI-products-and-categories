from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException


from main import get_db
from models.product_category import (
    ProductCategory,
    ProductCategoryCreate,
    ProductCategoryUpdate,
)
import scripts.product_category as crud_category

router_product_category = APIRouter()


# ============== CREATE ==============


@router_product_category.post("/category/", response_model=ProductCategory)
def create_product_category(
    category: ProductCategoryCreate, db: Session = Depends(get_db)
):
    db_category = crud_category.get_category_by_name(db, category_name=category.name)
    if db_category:
        raise HTTPException(
            status_code=400, detail="Category with same name already registered"
        )
    return crud_category.create_category(db, category=category)


# ============== READ ==============


@router_product_category.get("/categories/", response_model=list[ProductCategory])
def read_categories(db: Session = Depends(get_db)):
    categories = crud_category.get_categories(db=db, skip=0, limit=100)
    return categories


@router_product_category.get("/category/{category_id}", response_model=ProductCategory)
def read_category_by_id(category_id: int, db: Session = Depends(get_db)):
    db_category = crud_category.get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Product category not found")
    return db_category


@router_product_category.get("/category/", response_model=ProductCategory)
def read_category_by_name(category_name: str, db: Session = Depends(get_db)):
    db_category = crud_category.get_category_by_name(db=db, category_name=category_name)
    if db_category is None:
        raise HTTPException(
            status_code=404, detail="There is no category with that name"
        )
    return db_category


# ============== UPDATE ==============


@router_product_category.patch(
    "/category/{category_id}", response_model=ProductCategory
)
def update_category(
    category_id: int,
    category: ProductCategoryUpdate,
    db: Session = Depends(get_db),
):
    db_category = crud_category.get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Product category not found")
    return crud_category.update_category(
        db=db, category_id=category_id, category=category
    )


# ============== DELETE ==============


@router_product_category.delete(
    "/category/{category_id}", response_model=ProductCategory
)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud_category.get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Product category not found")
    return crud_category.delete_category(category_id=category_id, db=db)
