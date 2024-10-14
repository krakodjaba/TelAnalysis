from utils import remove_chars_from_text, remove_emojis, clear_user, read_conf
import nltk_analyse
import sys
from pywebio import config, output, pin, session
import json, re, jmespath
from validate_email import validate_email
import phonenumbers
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Глобальные переменные
emails, phoness, all_tokens, users = [], [], [], {}
count_messages = 0


action_map = {
    'invite_members': 'Invite Member',
    'remove_members': 'Kicked Members',
    'join_group_by_link': 'Joined by Link',
    'pin_message': 'Pinned Message',
    # Добавьте другие действия по необходимости
}

action_reverse   = ['Invite Member','Kicked Members','Joined by Link', 'Pinned Message']

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

with open(f'asset/{filename}.json', 'r', encoding='utf-8') as datas:
    data = json.load(datas)

sf = jmespath.search('messages[*]', data)
group_name = jmespath.search('name', data)

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

def extract_text_from_message(message):
    texts = set()  # Используем множество, чтобы избежать дубликатов
    
    if isinstance(message, dict):
        text = jmespath.search('text', message)
        if isinstance(text, str) and text.strip():
            texts.add(text)

        elif isinstance(text, list):
            for item in text:
                if isinstance(item, dict):
                    item = jmespath.search('text', item)
                    if item:
                        texts.add(item)
                elif isinstance(item, str):
                    texts.add(item)

        entities = jmespath.search('text_entities[*].text', message)
        if entities:
            for entity in entities:
                texts.add(entity)

        for value in message.values():
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
                    users[user].append((f"{action_text} - {members}",0.0))
                elif action == 'pin_message':
                    users[user].append((f"{action_text} - {tex}",0.0))
                else:
                    users[user].append((f"{action_text} {tex}",0.0))
                return

    user = user.replace(" ", "")
    if user not in users:
        users[user] = []
    count_messages += 1

    unique_texts = extract_text_from_message(message)
    for clean_text in unique_texts:
        if clean_text:
            #users[user].append(clean_text)
            sentiment_score = analyze_sentiment(clean_text)
            users[user].append((clean_text, sentiment_score))  # Сохраняем текст и балл
            # Извлечение email и телефонных номеров
            extracted_emails, extracted_phone_numbers = extract_emails_and_phone_numbers(clean_text)
            emails.extend(extracted_emails)
            phoness.extend(extracted_phone_numbers)

# Обработка сообщений с использованием потоковой обработки
with ThreadPoolExecutor() as executor:
    executor.map(process_message, sf)

# Теперь отображаем в нужном формате user - user_from
for user, da in users.items():
    #print(da)
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
    user_sentiment_scores = []
    for x in da:
        try:
            score = float(x[1])  # Приводим к float
            user_sentiment_scores.append(score)
        except (ValueError, TypeError):
            # Игнорируем элементы, которые не могут быть преобразованы в float
            #print(f"Invalid sentiment score: {x}")
            continue
    average_user_sentiment = sum(user_sentiment_scores) / len(user_sentiment_scores) if user_sentiment_scores else 0
    
    try:
        most_com = read_conf('most_com')
        genuy, tokens = nltk_analyse.analyse(da, most_com)

        gemy = [[x, y] for x, y in genuy]
        gery = [[x[0]] for x in da]
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
all_tokens, data = nltk_analyse.analyse_all(all_tokens, most_com)
all_chat = [[i[0], i[1]] for i in all_tokens]
output.put_collapse(f'TOP words of {group_name}', [
    output.put_table(all_chat, header=['word']),
], open=False)

all_sentiment_scores = [analyze_sentiment(msg) for msg in all_tokens]
average_chat_sentiment = sum(all_sentiment_scores) / len(all_sentiment_scores) if all_sentiment_scores else 0
output.put_text(f'Average Sentiment for {group_name}: {average_chat_sentiment:.2f}')


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
