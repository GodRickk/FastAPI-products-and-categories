from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def read_root():
    html_content = "<h4>Hello! It's main page</h4>"
    return HTMLResponse(content=html_content)


@app.get("/about")
def get_about():
    return {"message": "about site"}