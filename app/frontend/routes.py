from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the 'app' directory
app_dir = os.path.dirname(current_dir)
# Set the templates directory
templates_dir = os.path.join(app_dir, "templates")

templates = Jinja2Templates(directory=templates_dir)

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})