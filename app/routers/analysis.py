from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
import uuid
import asyncio
from ..services import channel_analyse, chat_analyse, graph_generator
import logging
logging.basicConfig(level=logging.DEBUG)
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/analyze/channel", response_class=HTMLResponse)
async def analyze_channel(request: Request, file: UploadFile = File(...)):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only .json files allowed")

    file_id = str(uuid.uuid4())
    saved_path = os.path.join(UPLOAD_DIR, f"{file_id}.json")
    with open(saved_path, "wb") as f:
        f.write(await file.read())

    # Анализ канала
    result = await asyncio.to_thread(channel_analyse.analyze_channel_file, saved_path)

    # Добавляем пути к результату, чтобы можно было использовать в result.html
    try:
        graph_data = await asyncio.to_thread(graph_generator.generate_graph_from_file, saved_path)
        result.update({
            "graph_json": graph_data['json']
        })
    except Exception as e:
        result.update({
            "graph_json": None,
            "graph_error": str(e)
        })


    return templates.TemplateResponse("result_channel.html", {"request": request, "result": result, "file_id": file_id}) 


@router.post("/analyze/chat", response_class=HTMLResponse)
async def analyze_chat(request: Request, file: UploadFile = File(...)):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only .json files allowed")

    file_id = str(uuid.uuid4())
    saved_path = os.path.join(UPLOAD_DIR, f"{file_id}.json")
    with open(saved_path, "wb") as f:
        f.write(await file.read())

    # Анализ чата
    result = await asyncio.to_thread(chat_analyse.analyze_chat_file, saved_path)

    try:
        graph_data = await asyncio.to_thread(graph_generator.generate_graph_from_file, saved_path)
        result.update({
            "graph_json": graph_data['json'],
        })
    except Exception as e:
        result.update({
            "graph_json": None,
            "graph_error": str(e)
        })


    return templates.TemplateResponse("result.html", {"request": request, "result": result, "file_id": file_id})
