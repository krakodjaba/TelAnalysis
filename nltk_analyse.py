import json
import re
import string
import collections
import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from utils import remove_chars_from_text, remove_emojis, read_conf
import stopwords_list

# Инициализация стеммера
stemmer = SnowballStemmer("russian")

# Специальные символы для очистки текста
spec_chars = string.punctuation + '\n\xa0«»\t—…"<>?!.,;:꧁@#$%^&*()_-+=№%༺༺\༺/༺-•'

# Действия, которые нужно игнорировать в тексте
action_map = ['Invite Member', 'Kicked Members', 'Joined by Link', 'Pinned Message']

def analyse(data, most_com):
    # Настройка стоп-слов
    russian_stopwords = stopwords.words("russian")
    russian_stopwords.extend(['это', 'ну', 'но', 'еще', 'ещё', 'оно', 'типа'])
    english_stopwords = stopwords.words("english")

    # Приведение текста к нижнему регистру и удаление лишних символов
    text = str(data).lower().replace("'", "").replace(",", "").replace("[", "").replace("]", "").replace("-", " ")
    
    for action in action_map:
        text = text.replace(action.lower(), "")
    
    text = remove_chars_from_text(text, spec_chars)
    text = remove_chars_from_text(text, string.digits)

    # Проверка, что текст не пустой
    if len(text) < 1:
        return [], []

    # Токенизация текста
    text_tokens = word_tokenize(text)

    # Стемминг токенов, если выбран
    if read_conf('select_type_stem') == 'On':
        text_tokens = [stemmer.stem(word) for word in text_tokens]

    # Фильтрация токенов
    text_tokens = [token.strip() for token in text_tokens if 
                   token not in russian_stopwords and 
                   len(token) >= 3 and 
                   len(token) < 26 and 
                   token not in english_stopwords and 
                   'http' not in token and 
                   token not in stopwords_list.stopword_txt]

    # Частотное распределение
    text = nltk.Text(text_tokens)
    fdist = FreqDist(text)
    fdist = fdist.most_common(most_com)

    return fdist, text_tokens

def analyse_all(data, most_com):
    # Настройка стоп-слов
    russian_stopwords = stopwords.words("russian")
    english_stopwords = stopwords.words("english")
    russian_stopwords.extend(['это', 'ну', 'но', 'еще', 'ещё', 'оно', 'типа'])

    # Приведение текста к нижнему регистру и удаление лишних символов
    text = str(data).lower().replace("'", "").replace(",", "").replace("[", "").replace("]", "").replace("-", " ")
    text = remove_chars_from_text(text, spec_chars)
    text = remove_chars_from_text(text, string.digits)
    #text = remove_emojis(text)

    if len(text) >= 1:
        text_tokens = word_tokenize(text)
    else:
        return [], []

    # Стемминг токенов, если выбран
    if read_conf('select_type_stem') == 'On':
        text_tokens = [stemmer.stem(word) for word in text_tokens]

    # Фильтрация токенов
    text_tokens = [token.strip() for token in text_tokens if 
                   token not in russian_stopwords and 
                   len(token) >= 4 and 
                   len(token) < 26 and 
                   token not in english_stopwords and 
                   'http' not in token and 
                   token not in stopwords_list.stopword_txt]

    # Частотное распределение
    text = nltk.Text(text_tokens)
    fdist = FreqDist(text)
    fdist = fdist.most_common(most_com)

    data = [i[0] for i in fdist]
    return fdist, data
