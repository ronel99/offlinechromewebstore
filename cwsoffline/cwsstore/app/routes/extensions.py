from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, Response
from fastapi.templating import Jinja2Templates
import os
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Path to the extensions JSON file
#EXTENSIONS_FILE = os.path.join(os.path.dirname(__file__), "../artifacts/extensions_info.json")
EXTENSIONS_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../artifacts/extensions_info.json")
)

@router.get("/json", response_class=FileResponse)
async def serve_extensions_info_xml():
    """Serve the extensions_info.xml file."""
    xml_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../artifacts/extensions_info.json"))
    if os.path.exists(xml_file_path):
        return FileResponse(xml_file_path, media_type="application/json")
    return JSONResponse(content={"error": "extensions_info.json not found"}, status_code=404)

@router.get("/crx", response_class=Response)
async def serve_extensions_info_xml(request: Request):
    """Serve the update.xml file rendered with Jinja2."""
    if os.path.exists(EXTENSIONS_FILE):
        with open(EXTENSIONS_FILE, "r") as file:
            extensions = json.load(file)
        xml_content = templates.get_template("update.xml").render(
            request=request, extensions=extensions
        )
        return Response(content=xml_content, media_type="application/xml")
    return JSONResponse(content={"error": "update.xml not found"}, status_code=404)

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the homepage with a list of extensions."""
    if os.path.exists(EXTENSIONS_FILE):
        with open(EXTENSIONS_FILE, "r") as file:
            extensions = json.load(file)
        return templates.TemplateResponse("index.html", {"request": request, "extensions": extensions})
    return JSONResponse(content={"error": f"Extensions file not found {EXTENSIONS_FILE}"}, status_code=404)

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