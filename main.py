from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse

# from . import crud, models, schemas
import crud, models, schemas
# from .database import SessionLocal, engine
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_name(db, product_name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product with same name already registred")
    return crud.create_product(db=db, product=product)


@app.post("/products-with-category/", response_model=schemas.Product)
def create_product_with_category(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_name(db, product_name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product with same name already registred")
    
    category = crud.get_category(db=db, category_id=product.category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="No such category")

    return crud.create_product_with_category(db=db, product=product)


@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.get("/product/", response_model=schemas.Product)
def read_product_by_name(product_name: str, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_name(db=db, product_name=product_name)
    if db_product is None:
        raise HTTPException(status_code=404, detail="There is no product with that name")
    return db_product


@app.patch("/product/{product_id}", response_model=schemas.ProductUpdate)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.update_product(db=db, product_id=product_id, product=product)


@app.delete("/product/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.delete_product(db=db, product_id=product_id)


@app.post("/categories/", response_model=schemas.ProductCategory)
def create_product_category(category: schemas.ProductCategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db, category_name=category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="Category with same name already registred")
    return crud.create_category(db, category=category)


@app.get("/categories/", response_model=list[schemas.ProductCategory])
def read_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db=db, skip=0, limit=100)
    return categories


@app.get("/categories/{category_id}", response_model=schemas.ProductCategory)
def read_category_by_id(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Product category not found")
    return db_category


@app.get("/category/", response_model=schemas.ProductCategory)
def read_category_by_name(category_name: str, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db=db, category_name=category_name)
    if db_category is None:
        raise HTTPException(status_code=404, detail="There is no category with that name")
    return db_category


@app.patch("/category/{category_id}", response_model=schemas.ProductCategory)
def update_category(category_id: int, category: schemas.ProductCategoryUpdate, db: Session = Depends(get_db)):
    db_category = crud.get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Product category not found")
    return crud.update_category(db=db, category_id=category_id, category=category)


@app.delete("/categoty/{category_id}", response_model=schemas.ProductCategory)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Product category not found")
    return delete_category(category_id=category_id, db=db)


@app.get("/")
def read_root():
    html_content = "<h4>Hello! It's main page</h4>"
    return HTMLResponse(content=html_content)


@app.get("/about")
def get_about():
    return {"message": "about site"}