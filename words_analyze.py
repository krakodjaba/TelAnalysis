from utils import remove_chars_from_text, remove_emojis, clear_user, read_conf
import nltk_analyse
import sys
from pywebio import config, output, pin, session
import json, re, jmespath
from validate_email import validate_email
import phonenumbers
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Глобальные переменные
emails, phoness, all_tokens, users = [], [], [], {}
count_messages = 0

# Карта действий для различных типов сообщений
action_map = {
    'invite_members': 'Invite Member',
    'remove_members': 'Kicked Members',
    'join_group_by_link': 'Joined by Link',
    'pin_message': 'Pinned Message',
    # Добавьте другие действия по необходимости
}

# Карта для обратного преобразования действий
action_reverse = ['Invite Member', 'Kicked Members', 'Joined by Link', 'Pinned Message']

# Инициализация анализатора тональности
analyzer = SentimentIntensityAnalyzer()

# Конфигурация интерфейса
config(theme='dark', title="TelAnalysis", description="Analysing Telegram CHATS-CHANNELS-GROUPS")
output.toast(content='Wait..', duration=2)
output.put_button("Scroll Down", onclick=lambda: session.run_js('window.scrollTo(0, document.body.scrollHeight)'))
output.put_button("Close", onclick=lambda: session.run_js('window.close()'), color='danger')
output.put_html("<h1><center>Analyse of Telegram Chat<center></h1><br>")

# Ввод ID пользователя
pin.put_input('ID')
output.put_button("Search ID", onclick=lambda: session.run_js(f'window.find({pin.pin.ID}, true)'), color='warning')

# Открытие файла и загрузка данных
filename = sys.argv[1].split(".")[0].split("/")[1]

# Убедимся, что файл открыт с корректной кодировкой
with open(f'asset/{filename}.json', 'r', encoding='utf-8', errors='replace') as datas:
    data = json.load(datas)

sf = jmespath.search('messages[*]', data)
group_name = jmespath.search('name', data)

# Функция для анализа тональности
def analyze_sentiment(text):
    try:
        score = analyzer.polarity_scores(str(text))
        return float(score['compound'])  # Приводим к float для уверенности
    except:
        return float(0.0)

# Функция для извлечения email и телефонных номеров из текста
def extract_emails_and_phone_numbers(text):
    emails_list = []
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    for email in emails:
        if validate_email(email, verify=False):
            emails_list.append(email)
    phones_list = []    
    phone_numbers = re.findall(r'\+?[0-9]{1,3}?[-. (]?[0-9]{1,4}[-. )]?[0-9]{1,4}[-. ]?[0-9]{1,9}', text)
    for phones in phone_numbers:
        try:
            phone_number = phonenumbers.parse(phones, None)
            if phonenumbers.is_valid_number(phone_number):
                phones_list.append(phones)
        except Exception:
            pass       
    return emails_list, phones_list

# Функция для извлечения текста из сообщения с улучшенной обработкой вложенных структур
def extract_text_from_message(message):
    texts = set()  # Используем множество для уникальных значений текста

    if isinstance(message, dict):
        # Извлекаем все возможные поля с текстом напрямую
        if 'text' in message:
            if isinstance(message['text'], str) and message['text'].strip():
                texts.add(message['text'])
            elif isinstance(message['text'], list):  # Если "text" - это список
                for item in message['text']:
                    if isinstance(item, str):
                        texts.add(item)
        
        # Извлечение текста из других полей, таких как caption для медиа
        if 'caption' in message:
            if isinstance(message['caption'], str) and message['caption'].strip():
                texts.add(message['caption'])
        
        # Ищем текстовые сущности в text_entities
        entities = jmespath.search('text_entities[*].text', message)
        if entities:
            for entity in entities:
                texts.add(entity)

        # Обрабатываем вложенные структуры: пересланные и ответы на сообщения
        if 'forwarded_from' in message:
            texts.update(extract_text_from_message(message['forwarded_from']))

        if 'reply_to_message' in message:
            texts.update(extract_text_from_message(message['reply_to_message']))

        # Рекурсивно обрабатываем вложенные структуры
        for key, value in message.items():
            if isinstance(value, (list, dict)):
                texts.update(extract_text_from_message(value))

    elif isinstance(message, list):
        for item in message:
            texts.update(extract_text_from_message(item))

    return texts

# Функция для обработки каждого сообщения
def process_message(message):
    global count_messages
    action = ""
    user = jmespath.search('from_id', message)

    if not user:
        user = jmespath.search('actor_id', message)
        if user:
            user = user.replace(" ", "")
            if user not in users:
                users[user] = []

            action = jmespath.search('action', message)
            if action:
                tex = jmespath.search('text', message) or ''
                action_text = action_map.get(action, action)
                
                if action in ['invite_members', 'remove_members']:
                    members = jmespath.search('members', message)
                    members = ",".join(str(x) for x in members if x)
                    users[user].append((f"{action_text} - {members}", 0.0))
                else:
                    users[user].append((f"{action_text} {tex}", 0.0))
                return

    user = user.replace(" ", "")
    if user not in users:
        users[user] = []
    count_messages += 1

    unique_texts = extract_text_from_message(message)
    for clean_text in unique_texts:
        if clean_text:
            sentiment_score = analyze_sentiment(clean_text)
            users[user].append((clean_text, sentiment_score))  # Сохраняем текст и балл
            # Извлечение email и телефонных номеров
            extracted_emails, extracted_phone_numbers = extract_emails_and_phone_numbers(clean_text)
            emails.extend(extracted_emails)
            phoness.extend(extracted_phone_numbers)

# Обработка сообщений с использованием потоковой обработки
with ThreadPoolExecutor() as executor:
    future_to_message = {executor.submit(process_message, msg): msg for msg in sf}
    for future in as_completed(future_to_message):  # Используем as_completed правильно
        try:
            future.result()  # Проверка завершения каждого потока
        except Exception as e:
            print(f"Error processing message: {e}")

# Теперь отображаем в нужном формате user - user_from
for user, da in users.items():
    user_from = ""
    messages = jmespath.search(f"messages[*]", data)
    
    for m in messages:
        if jmespath.search('from_id', m) == user:
            user_from = jmespath.search('from', m)
            break
    
    if user_from:
        user_display = f"{user_from} - {user}"
    else:
        user_display = user
        
    # Извлечение оценок чувствительности
    user_sentiment_scores = [float(x[1]) for x in da if isinstance(x[1], float)]
    average_user_sentiment = sum(user_sentiment_scores) / len(user_sentiment_scores) if user_sentiment_scores else 0
    
    try:
        most_com = read_conf('most_com')
        genuy, tokens = nltk_analyse.analyse(da, most_com)

        gemy = [[x, y] for x, y in genuy]
        gery = [[x[0]] for x in da]
        #print(len(all_tokens))
        all_tokens.extend(tokens)

        if gery or gemy:
            output.put_collapse(user_display, [
        f'Messages of {user_display}',  # Сообщение с user_from
        output.put_text(f'Average Sentiment for {user_display}: {average_user_sentiment:.2f}'),
        output.put_table([[x[0], x[1]] for x in da], header=['Messages', 'Sentiment Score']),
        output.put_table(gemy, header=['word', 'count'])
    ], open=False)

    except Exception as ex:
        print(f"[{user}] error: {ex}")

# Общий анализ всех сообщений
most_com = read_conf('most_com')

# Проверяем, что функция nltk_analyse.analyse_all возвращает правильные данные
try:
    all_tokens, data = nltk_analyse.analyse_all(all_tokens, most_com)
except Exception as e:
    print(f"Error in analyse_all: {e}")

# Проверим, что all_tokens не пустой
if all_tokens:
    all_chat = [[i[0], i[1]] for i in all_tokens]
    output.put_collapse(f'TOP words of {group_name}', [
        output.put_table(all_chat, header=['word']),
    ], open=False)

    # Общий анализ тональности чата
    all_sentiment_scores = [analyze_sentiment(msg[0]) for msg in all_tokens]  # Извлекаем текст для анализа
    average_chat_sentiment = sum(all_sentiment_scores) / len(all_sentiment_scores) if all_sentiment_scores else 0
    output.put_text(f'Average Sentiment for {group_name}: {average_chat_sentiment:.2f}')
else:
    #print("No tokens found for analysis.")
    output.put_text(f"No tokens found for {group_name}. Sentiment analysis is unavailable.")


# Обработка email и телефонов
emaills = [[email] for email in set(emails)]
phonness = [[ph] for ph in set(phoness)]
output.put_collapse('Finded Emails and Numbers', [
    output.put_table(emaills, header=['Emails:']),
    output.put_table(phonness, header=['Numbers:'])
], open=False)

# Дополнительные кнопки
output.put_button("Close", onclick=lambda: session.run_js('window.close()'), color='danger')
output.put_button("Scroll Up", onclick=lambda: session.run_js('window.scrollTo(document.body.scrollHeight, 0)'))
