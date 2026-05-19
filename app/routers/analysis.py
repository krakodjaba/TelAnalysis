from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
import uuid
import asyncio
from pathlib import Path
from ..services import channel_analyse, chat_analyse, graph_generator, semantic_analyse, stylometric_analyse, temporal_analyse
import logging
logging.basicConfig(level=logging.DEBUG)
router = APIRouter()

# Detect if running in Docker or on host
if Path("/app").exists() and Path("/.dockerenv").exists():
    BASE_DIR = Path("/app")
else:
    BASE_DIR = Path(__file__).parent.parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/analyze/channel", response_class=HTMLResponse)
async def analyze_channel(request: Request, file: UploadFile = File(...)):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only .json files allowed")

    file_id = str(uuid.uuid4())
    saved_path = UPLOAD_DIR / f"{file_id}.json"
    with open(saved_path, "wb") as f:
        f.write(await file.read())

    # Анализ канала
    result = await asyncio.to_thread(channel_analyse.analyze_channel_file, saved_path)

    # Добавляем семантический анализ
    try:
        semantic_result = await asyncio.to_thread(semantic_analyse.semantic_analysis_from_file, saved_path)
        result.update({
            "semantic": semantic_result
        })
    except Exception as e:
        result.update({
            "semantic": None,
            "semantic_error": str(e)
        })

    # Добавляем стилометрический анализ
    try:
        # Extract text messages for stylometric analysis
        import json
        with open(saved_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
        import jmespath
        messages = jmespath.search('messages[*].text', data) or []
        text_messages = []
        for msg in messages:
            if isinstance(msg, str):
                text_messages.append(msg)
            elif isinstance(msg, list):
                for item in msg:
                    if isinstance(item, str):
                        text_messages.append(item)
        
        if text_messages:
            stylometric_result = await asyncio.to_thread(stylometric_analyse.stylometric_analysis_from_messages, text_messages)
            result.update({
                "stylometric": stylometric_result
            })
    except Exception as e:
        result.update({
            "stylometric": None,
            "stylometric_error": str(e)
        })

    # Добавляем временной анализ
    try:
        temporal_result = await asyncio.to_thread(temporal_analyse.temporal_analysis_from_file, saved_path)
        result.update({
            "temporal": temporal_result
        })
    except Exception as e:
        result.update({
            "temporal": None,
            "temporal_error": str(e)
        })

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
    saved_path = UPLOAD_DIR / f"{file_id}.json"
    with open(saved_path, "wb") as f:
        f.write(await file.read())

    # Анализ чата
    result = await asyncio.to_thread(chat_analyse.analyze_chat_file, saved_path)

    # Добавляем семантический анализ
    try:
        semantic_result = await asyncio.to_thread(semantic_analyse.semantic_analysis_from_file, saved_path)
        result.update({
            "semantic": semantic_result
        })
    except Exception as e:
        result.update({
            "semantic": None,
            "semantic_error": str(e)
        })

    # Добавляем стилометрический анализ
    try:
        # Extract text messages for stylometric analysis
        import json
        with open(saved_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
        import jmespath
        messages = jmespath.search('messages[*].text', data) or []
        text_messages = []
        for msg in messages:
            if isinstance(msg, str):
                text_messages.append(msg)
            elif isinstance(msg, list):
                for item in msg:
                    if isinstance(item, str):
                        text_messages.append(item)
        
        if text_messages:
            stylometric_result = await asyncio.to_thread(stylometric_analyse.stylometric_analysis_from_messages, text_messages)
            result.update({
                "stylometric": stylometric_result
            })
    except Exception as e:
        result.update({
            "stylometric": None,
            "stylometric_error": str(e)
        })

    # Добавляем временной анализ
    try:
        temporal_result = await asyncio.to_thread(temporal_analyse.temporal_analysis_from_file, saved_path)
        result.update({
            "temporal": temporal_result
        })
    except Exception as e:
        result.update({
            "temporal": None,
            "temporal_error": str(e)
        })

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
