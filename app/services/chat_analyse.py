import json
import jmespath
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from . import nltk_analyse, utils
from .utils import remove_chars_from_text, remove_emojis, read_conf, stopword_txt

analyzer = SentimentIntensityAnalyzer()
stopword_set = set(stopword_txt)


def analyze_sentiment(text):
    try:
        score = analyzer.polarity_scores(str(text))
        return float(score['compound'])
    except:
        return 0.0


def clean_text_for_analysis(text):
    text = remove_emojis(text)
    text = remove_chars_from_text(text)
    text = text.lower()
    text = ' '.join([w for w in text.split() if w not in stopword_set])
    return text.strip()


def extract_emails_and_phone_numbers(text):
    import re
    emails_list = []
    phones_list = []
    for email in re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text):
        emails_list.append(email)
    # телефоны — простая вырезка; подробная валидация опущена
    for ph in re.findall(r'\+?[0-9]{6,15}', text):
        phones_list.append(ph)
    return emails_list, phones_list


def extract_text_from_message(message):
    texts = set()
    if isinstance(message, dict):
        if 'text' in message:
            if isinstance(message['text'], str) and message['text'].strip():
                texts.add(message['text'])
            elif isinstance(message['text'], list):
                for item in message['text']:
                    if isinstance(item, str):
                        texts.add(item)
        if 'caption' in message and isinstance(message['caption'], str):
            texts.add(message['caption'])
        entities = jmespath.search('text_entities[*].text', message)
        if entities:
            texts.update(entities)
        if 'forwarded_from' in message:
            texts.update(extract_text_from_message(message['forwarded_from']))
        if 'reply_to_message' in message:
            texts.update(extract_text_from_message(message['reply_to_message']))
        for key, value in message.items():
            if isinstance(value, (list, dict)):
                texts.update(extract_text_from_message(value))
    elif isinstance(message, list):
        for item in message:
            texts.update(extract_text_from_message(item))
    return texts


def process_message(message, users, emails_set, phones_set, count_messages_ref):
    action_map = {
        'invite_members': 'Invite Member',
        'remove_members': 'Kicked Members',
        'join_group_by_link': 'Joined by Link',
        'pin_message': 'Pinned Message',
    }

    user = jmespath.search('from_id', message) or jmespath.search('actor_id', message)
    if not user:
        return

    user = str(user).replace(" ", "")
    users.setdefault(user, [])

    action = jmespath.search('action', message)
    if action:
        tex = jmespath.search('text', message) or ''
        action_text = action_map.get(action, action)
        if action in ['invite_members', 'remove_members']:
            members = jmespath.search('members', message) or []
            members = ",".join(str(x) for x in members if x)
            users[user].append((f"{action_text} - {members}", 0.0))
        else:
            users[user].append((f"{action_text} {tex}", 0.0))
        return

    count_messages_ref[0] += 1
    unique_texts = extract_text_from_message(message)
    for text in unique_texts:
        if text:
            t = clean_text_for_analysis(text)
            if not t:
                continue
            sentiment = analyze_sentiment(t)
            users[user].append((t, sentiment))
            e, p = extract_emails_and_phone_numbers(t)
            emails_set.update(e)
            phones_set.update(p)


def analyze_chat_file(filepath: str) -> dict:
    """
    Анализ чата: читает uploads/*.json и возвращает словарь с результатами:
      - group_name
      - users: { user_id: { display_name, messages:[(text,sentiment)], avg_sentiment } }
      - top_words: list
      - emails, phones
    """
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        data = json.load(f)

    sf = jmespath.search('messages[*]', data) or []
    group_name = jmespath.search('name', data) or os.path.basename(filepath)

    emails_set = set()
    phones_set = set()
    all_tokens = []
    users = {}
    count_messages = [0]  # mutable ref for threads

    # Параллельная обработка сообщений
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_message, msg, users, emails_set, phones_set, count_messages) for msg in sf]
        for future in futures:
            try:
                future.result()
            except Exception:
                pass

    # Собираем результаты по пользователям
    users_out = {}
    for user_id, da in users.items():
        # попробуем получить display name из первых сообщений
        user_from = ""
        for m in sf:
            if jmespath.search('from_id', m) == user_id:
                user_from = jmespath.search('from', m)
                break
        user_display = f"{user_from} - {user_id}" if user_from else user_id
        scores = [x[1] for x in da if isinstance(x[1], float)]
        avg_sentiment = sum(scores)/len(scores) if scores else 0.0

        # частотный анализ по сообщениям пользователя
        try:
            most_com = read_conf('most_com') or 30
            genuy, tokens = nltk_analyse.analyse(da, most_com)
            all_tokens.extend(tokens)
            users_out[user_id] = {
                "display": user_display,
                "messages": da,
                "avg_sentiment": avg_sentiment,
                "top_words": [[x[0], x[1]] for x in genuy]
            }
        except Exception:
            users_out[user_id] = {
                "display": user_display,
                "messages": da,
                "avg_sentiment": avg_sentiment,
                "top_words": []
            }

    # Общий анализ
    try:
        most_com = read_conf('most_com') or 30
        all_tokens_fdist, top_words = nltk_analyse.analyse_all(all_tokens, most_com)
    except Exception:
        top_words = []
    print(
        {
        "group_name": group_name,
        "users": users_out,
        "top_words": top_words,
        "emails": list(emails_set),
        "phones": list(phones_set),
        "count_messages": count_messages[0]
    }
    )
    return {
        "group_name": group_name,
        "users": users_out,
        "top_words": top_words,
        "emails": list(emails_set),
        "phones": list(phones_set),
        "count_messages": count_messages[0]
    }
