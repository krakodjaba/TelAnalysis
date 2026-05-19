from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from .routers import analysis
import os
import logging
logging.basicConfig(level=logging.DEBUG)


app = FastAPI(title="Telanalysis FastAPI")
from pathlib import Path

# Detect if running in Docker or on host
if Path("/app").exists() and Path("/.dockerenv").exists():
    # Running in Docker container
    BASE_DIR = Path("/app")
    STATIC_DIR = BASE_DIR / "app" / "static"
    TEMPLATES_DIR = BASE_DIR / "app" / "templates"
else:
    # Running on host
    BASE_DIR = Path(__file__).parent.parent
    STATIC_DIR = BASE_DIR / "app" / "static"
    TEMPLATES_DIR = BASE_DIR / "app" / "templates"

GRAPHS_DIR = BASE_DIR / "graphs"
UPLOADS_DIR = BASE_DIR / "uploads"

GRAPHS_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/graphs", StaticFiles(directory=str(GRAPHS_DIR)), name="graphs")
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

# Папка static
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")



templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Подключаем роутер
app.include_router(analysis.router, prefix="")

# CORS (для примера открыт; в продакшне укажи конкретные домены)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
