from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from .routers import analysis
import os
import logging
logging.basicConfig(level=logging.DEBUG)


app = FastAPI(title="Telanalysis FastAPI")

# Папка uploads
# Папка graphs
os.makedirs("graphs", exist_ok=True)
app.mount("/graphs", StaticFiles(directory="graphs"), name="graphs")

# Папка uploads
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Папка static
app.mount("/static", StaticFiles(directory="app/static"), name="static")



templates = Jinja2Templates(directory="app/templates")

# Подключаем роутер
app.include_router(analysis.router, prefix="")

# CORS (для примера открыт; в продакшне укажи конкретные домены)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
