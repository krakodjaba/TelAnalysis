import re
import string
import emoji
import json
import os
from pathlib import Path

SPEC_CHARS = string.punctuation + '\n\xa0«»\t—…"<>?!.,;:꧁@#$%^&*()_+=№%༺༺\\༺/༺•'

# Detect if running in Docker or on host
if Path("/app").exists() and Path("/.dockerenv").exists():
    BASE_DIR = Path("/app")
else:
    BASE_DIR = Path(__file__).parent.parent.parent

CONFIG_FILE = BASE_DIR / "config.json"


def read_conf(option: str):
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            conf = json.load(f)
        # простая безопасная выдача
        return conf.get(option)
    except (FileNotFoundError, json.JSONDecodeError):
        default_conf = {"select_type_stem": "Off", "most_com": 30, "most_com_channel": 100}
        write_conf(default_conf)
        return default_conf.get(option)


def write_conf(dct: dict):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as fw:
            json.dump(dct, fw, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[ERROR] Cannot write config: {e}")


def remove_chars_from_text(text: str, char: str = None) -> str:
    if not isinstance(text, str):
        text = str(text)
    char = char or SPEC_CHARS
    text = re.sub(f"[{re.escape(char)}]", " ", text)
    return re.sub(r'\s+', ' ', text).strip()


def remove_emojis(data: str) -> str:
    if not isinstance(data, str):
        data = str(data)
    data = emoji.replace_emoji(data, replace='')
    data = re.sub(r'[\x00-\x1F\x7F-\x9F]+', '', data)
    data = remove_chars_from_text(data, SPEC_CHARS)
    data = re.sub(r'\s+', ' ', data).strip()
    return data


def clear_uploads_older_than(days: int = 7, folder: str = "uploads"):
    import time
    now = time.time()
    cutoff = now - days * 86400
    for root, _, files in os.walk(folder):
        for fname in files:
            path = os.path.join(root, fname)
            try:
                if os.path.getmtime(path) < cutoff:
                    os.remove(path)
            except Exception:
                pass

stopword_txt = [
    "а", "без", "белый", "больше", "большой", "будем", "будет", "будешь", 
    "буду", "будут", "будь", "бы", "бывает", "был", "была", "были", 
    "было", "в", "ваш", "всем", "всех", "всего", "вы", "где", 
    "да", "даже", "два", "долго", "друг", "для", "е", "его", "ее", 
    "ей", "ему", "если", "есть", "здесь", "или", "им", "к", 
    "как", "когда", "кого", "ком", "кто", "мы", "на", "наш", "не", 
    "нет", "ни", "один", "одиннадцать", "она", "они", "оно", "опять", 
    "от", "по", "потом", "просто", "с", "сам", "свой", "так", "также", 
    "там", "тебя", "только", "у", "хотя", "что", "чтобы", "я", 
    "являюсь", "это", "этого", "этой", "этим", "такой", "все еще", 
    "весь", "где-то", "зачем", "чуть", "вместе", "сейчас", "тоже", 
    "другой", "вдруг", "и т.д."
]

# Для быстрого поиска можно использовать множество
stopword_set = list(set(stopword_txt))
