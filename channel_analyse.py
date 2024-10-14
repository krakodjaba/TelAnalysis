import json
import jmespath
import nltk_analyse
import utils
import time
from pywebio import input, config
from pywebio.output import put_html, put_text, put_image, put_table
from wordcloud import WordCloud


# Чтение конфигурации
select_type_stem = utils.read_conf('select_type_stem')
most_com = utils.read_conf('most_com_channel')

def channel(filename):
    # Извлечение имени канала из файла
    filename = filename.split(".")[0].split("/")[1]
    with open(f'asset/{filename}.json', 'r', encoding='utf-8') as f:
        jsondata = json.load(f)
        name_channel = jmespath.search('name', jsondata)

        # Отображение имени канала
        put_html(f"<center><h1>{name_channel}</h1></center>")
        messages_find = jmespath.search('messages[*].text', jsondata)

        text_list = []
        
        # Обработка сообщений канала
        for message in messages_find:
            if isinstance(message, list):
                for mes in message:
                    text = jmespath.search('text', mes) or mes
                    text_list.append(utils.remove_emojis(text))
            else:
                message = message.replace("   ", " ").replace("\n", "").replace("\t", "").strip()
                if len(message) > 4:
                    text_list.append(utils.remove_emojis(message))

        # Анализ текста и генерация облака слов
        fdist, tokens = nltk_analyse.analyse(text_list, most_com)
        all_tokens = list(tokens)
        all_tokens, data = nltk_analyse.analyse_all(all_tokens, most_com)
        
        # Генерация облака слов
        text_raw = " ".join(data)
        wordcloud = WordCloud().generate(text_raw)
        filename_path = f'asset/{filename}_wordcloud.png'
        wordcloud.to_file(filename_path)


        # Отображение результата
        with open(filename_path, 'rb') as img_file:
            img = img_file.read()
        
        time.sleep(2)
        put_text(f"Wordcloud[{most_com}]:")
        put_image(img, width='600px')
        put_text(f"\nCount of all tokens: {len(tokens)}")
        put_text(f"\nСhannel frequency analysis[{most_com}]:")

        # Форматирование данных для таблицы
        gemy = [[x, y] for x, y in all_tokens]
        put_table(gemy, header=['word', 'count'])
