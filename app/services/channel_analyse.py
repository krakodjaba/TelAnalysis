import json
import jmespath
import time
import os
from wordcloud import WordCloud
from . import nltk_analyse, utils

def analyze_channel_file(filepath: str) -> dict:
    """
    Анализ файла канала из uploads/*.json
    Возвращает dict с ключами:
      - name_channel
      - wordcloud_path (путь к PNG)
      - total_tokens
      - top_words (list of [word,count])
    """
    # извлекаем имя канала (имя файла без расширения)
    filename = os.path.basename(filepath).split(".")[0]
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        jsondata = json.load(f)
    name_channel = jmespath.search('name', jsondata) or filename

    messages_find = jmespath.search('messages[*].text', jsondata)
    text_list = []

    for message in messages_find or []:
        if isinstance(message, list):
            for item in message:
                text = jmespath.search('text', item) or str(item)
                if text:
                    text_list.append(utils.remove_emojis(text.strip()))
        elif isinstance(message, str):
            message = message.replace("\n", " ").replace("\t", " ").strip()
            if len(message) > 4:
                text_list.append(utils.remove_emojis(message))

    if not text_list:
        return {"name_channel": name_channel, "error": "No messages found for analysis."}

    most_com = utils.read_conf('most_com_channel') or 100
    fdist, tokens = nltk_analyse.analyse(text_list, most_com)
    all_tokens, data = nltk_analyse.analyse_all(tokens, most_com)

    text_raw = " ".join(data)
    wc = WordCloud(width=800, height=400, background_color='white').generate(text_raw)

    out_dir = "graphs"
    os.makedirs(out_dir, exist_ok=True)
    wc_path = os.path.join(out_dir, f"{filename}_wordcloud.png")
    wc.to_file(wc_path)

    gemy = [[word, count] for word, count in all_tokens]

    return {
        "name_channel": name_channel,
        "wordcloud_path": wc_path,
        "total_tokens": len(tokens),
        "top_words": gemy
    }
