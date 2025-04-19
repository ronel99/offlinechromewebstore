from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Request
import os
import json

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
    if os.path.exists(extensions_file):
        with open(extensions_file, "r") as file:
            extensions = json.load(file)
        return templates.TemplateResponse("index.html", {"request": request, "extensions": extensions})
    return templates.TemplateResponse("index.html", {"request": request, "extensions": []})