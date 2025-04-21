from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Request
import os
import json
from datetime import datetime

app = FastAPI()

# Set up templates and static files
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routes
from app.routes.extensions import router as extensions_router
app.include_router(extensions_router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the homepage with a list of extensions."""
    extensions_file = os.path.join("app/static/extensions_info.json")
    current_year = datetime.now().year
    
    if os.path.exists(extensions_file):
        with open(extensions_file, "r") as file:
            extensions = json.load(file)
        print(current_year)
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "extensions": extensions,
            "current_year": current_year
        })
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "extensions": [],
        "current_year": current_year
    })