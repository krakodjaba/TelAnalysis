import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import string
from utils import remove_chars_from_text,remove_emojis
from nltk.corpus import stopwords
import stopwords_list
from pywebio import start_server, input, config
from pywebio.output import put_html,put_text,put_image, put_button, put_code, clear, put_file
from pywebio.input import file_upload as file
from pywebio.session import run_js
import json, re, jmespath, string, collections
from utils import remove_chars_from_text, remove_emojis, clear_user
import nltk_analyse
import networkx as nx
import matplotlib.pyplot as plt


spec_chars = string.punctuation + '\n\xa0«»\t—…"<>?!.,;:꧁@#$%^&*()_-+=№%༺༺\༺/༺-•'
def analyse(data):
    russian_stopwords = stopwords.words("russian")
    russian_stopwords.extend(['это','ну','но','еще','ещё','оно','типа'])
    english_stopwords = stopwords.words("english")
    text = str(data).lower().replace("'","").replace(",","").replace("[","").replace("]","").replace("-"," ")
    #print(text)
    text = remove_chars_from_text(text, spec_chars)
    text = remove_chars_from_text(text, string.digits)
    text = remove_emojis(text)
    text_tokens = word_tokenize(text)
    text_tokens = [token.strip() for token in text_tokens if token not in russian_stopwords and len(token) >= 2 and len(token) < 26 and token not in english_stopwords and 'http' not in token and token not in stopwords_list.stopword_txt]
    text = nltk.Text(text_tokens)
    #print(text)
    fdist = FreqDist(text)
    fdist = fdist.most_common(30)
    #
    #print(fdist)
    return fdist, text_tokens

def analyse_all(data):
    russian_stopwords = stopwords.words("russian")
    english_stopwords = stopwords.words("english")
    russian_stopwords.extend(['это','ну','но','еще','ещё','оно','типа'])
    text = str(data).lower().replace("'","").replace(",","").replace("[","").replace("]","").replace("-"," ")
    #print(text)
    text = remove_chars_from_text(text, spec_chars)
    text = remove_chars_from_text(text, string.digits)
    text = remove_emojis(text)
    text_tokens = word_tokenize(text)
    #print(text_tokens)
    text_tokens = [token.strip() for token in text_tokens if token not in russian_stopwords and len(token) >= 2 and len(token) < 26 and token not in english_stopwords and 'http' not in token and token not in stopwords_list.stopword_txt]
    text = nltk.Text(text_tokens)
    fdist = FreqDist(data)
    fdist = fdist.most_common(30)
    #
    #print(fdist)
    return fdist
