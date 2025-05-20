import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# ... (keep the existing imports and configurations)

# Configure Jinja2 templates
templates_dir_in_app = os.path.join(os.path.dirname(__file__), 'templates')
templates_dir_in_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')

if os.path.exists(templates_dir_in_app) and os.listdir(templates_dir_in_app):
    templates = Jinja2Templates(directory=templates_dir_in_app)
    logger.info(f"Using templates directory at {templates_dir_in_app}")
elif os.path.exists(templates_dir_in_root) and os.listdir(templates_dir_in_root):
    templates = Jinja2Templates(directory=templates_dir_in_root)
    logger.info(f"Using templates directory at {templates_dir_in_root}")
else:
    templates = None
    logger.warning(f"No templates found in {templates_dir_in_app} or {templates_dir_in_root}")

# ... (keep the existing code)

@app.get("/")
async def read_root(request: Request):
    logger.info("Root endpoint accessed.")
    if templates:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return {"message": "Welcome to the FastAPI application!"}

# ... (keep the rest of the file as is)