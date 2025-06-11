from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException


from main import get_db
from models.product import Product, ProductCreate, ProductUpdate
import scripts.product as crud_product


router_product = APIRouter()


# ============== CREATE ==============


@router_product.post("/product/", response_model=ProductCreate)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = crud_product.get_product_by_name(db, product_name=product.name)
    if db_product:
        raise HTTPException(
            status_code=400, detail="Product with same name already registred"
        )
    return crud_product.create_product(db=db, product=product)


@router_product.post("/product-with-category/", response_model=ProductCreate)
def create_product_with_category(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = crud_product.get_product_by_name(db, product_name=product.name)
    if db_product:
        raise HTTPException(
            status_code=400, detail="Product with same name already registred"
        )

    category = crud_product.get_category(db=db, category_id=product.category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="No such category")

    return crud_product.create_product_with_category(db=db, product=product)


# ============== READ ==============


@router_product.get("/products/", response_model=list[Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    min_price: int = None,
    max_price: int = None,
    min_amount: int = None,
    max_amount: int = None,
    category_id: int = None,
    db: Session = Depends(get_db),
):
    products = crud_product.get_products_with_filters(
        db=db,
        skip=skip,
        limit=limit,
        min_price=min_price,
        max_price=max_price,
        min_amount=min_amount,
        max_amount=max_amount,
        category_id=category_id,
    )
    return products


@router_product.get("/product/{product_id}", response_model=Product)
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router_product.get("/product/", response_model=Product)
def read_product_by_name(product_name: str, db: Session = Depends(get_db)):
    db_product = crud_product.get_product_by_name(db=db, product_name=product_name)
    if db_product is None:
        raise HTTPException(
            status_code=404, detail="There is no product with that name"
        )
    return db_product


# ============== UPDATE ==============


@router_product.patch("/product/{product_id}", response_model=ProductUpdate)
def update_product(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
):
    db_product = crud_product.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud_product.update_product(db=db, product_id=product_id, product=product)


# ============== DELETE ==============


@router_product.delete("/product/{product_id}", response_model=Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud_product.delete_product(db=db, product_id=product_id)
