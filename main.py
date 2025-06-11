from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from routers.product import router_product
from routers.product_category import router_product_category

from database import SessionLocal, engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router_product)
app.include_router(router_product_category)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    html_content = "<h4>Hello! It's main page</h4>"
    return HTMLResponse(content=html_content)


@app.get("/about")
def get_about():
    return {"message": "about site"}
