from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Path to the extensions JSON file
EXTENSIONS_FILE = os.path.join(os.path.dirname(__file__), "../static/extensions_info.json")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the homepage with a list of extensions."""
    if os.path.exists(EXTENSIONS_FILE):
        with open(EXTENSIONS_FILE, "r") as file:
            extensions = json.load(file)
        return templates.TemplateResponse("index.html", {"request": request, "extensions": extensions})
    return JSONResponse(content={"error": "Extensions file not found"}, status_code=404)

@router.get("/{extension_id}", response_class=HTMLResponse)
async def get_extension(request: Request, extension_id: str):
    """Render the details of a specific extension."""
    if os.path.exists(EXTENSIONS_FILE):
        with open(EXTENSIONS_FILE, "r") as file:
            extensions = json.load(file)
        if isinstance(extensions, list):  # Ensure it's a list of dictionaries
            for extension in extensions:
                if extension.get("extension_id") == extension_id:
                    return templates.TemplateResponse("extension.html", {"request": request, "extension": extension})
    return JSONResponse(content={"error": "Extension not found"}, status_code=404)

@router.get("/extensions/{extension_id}")
def fetch_extension(extension_id: str):
    """Fetch details of a specific extension by ID."""
    if os.path.exists(EXTENSIONS_FILE):
        with open(EXTENSIONS_FILE, "r") as file:
            extensions = json.load(file)
        if isinstance(extensions, list):  # Ensure it's a list of dictionaries
            for extension in extensions:
                if extension.get("extension_id") == extension_id:
                    return extension
        raise HTTPException(status_code=404, detail="Extension not found")
    raise HTTPException(status_code=404, detail="Extensions file not found")

@router.get("/download/{extension_id}")
async def download_extension(extension_id: str):
    """Download the CRX file for a specific extension."""
    if os.path.exists(EXTENSIONS_FILE):
        with open(EXTENSIONS_FILE, "r") as file:
            extensions = json.load(file)
        if isinstance(extensions, list):  # Ensure it's a list of dictionaries
            for extension in extensions:
                if extension.get("extension_id") == extension_id:
                    crx_path = os.path.join(os.path.dirname(__file__), "../static", extension["crx_url"].lstrip("/"))
                    if os.path.exists(crx_path):
                        return FileResponse(crx_path, media_type="application/octet-stream", filename=f"{extension_id}.crx")
                    return JSONResponse(content={"error": "CRX file not found"}, status_code=404)
    return JSONResponse(content={"error": "Extension not found"}, status_code=404)