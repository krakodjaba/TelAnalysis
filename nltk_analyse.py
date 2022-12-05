import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import string
from utils import remove_chars_from_text
from nltk.corpus import stopwords
import stopwords_list


def analyse(data):
    spec_chars = string.punctuation + '\n\xa0«»\t—…"<>?!.,;:'
    russian_stopwords = stopwords.words("russian")
    russian_stopwords.extend(['это','ну','но','еще','ещё','оно','типа'])
    english_stopwords = stopwords.words("english")
    text = str(data).lower().replace("'","").replace(",","").replace("[","").replace("]","").replace("-"," ")
    #print(text)
    text = remove_chars_from_text(text, spec_chars)
    text = remove_chars_from_text(text, string.digits)
    text_tokens = word_tokenize(text)
    text_tokens = [token.strip() for token in text_tokens if token not in russian_stopwords and len(token) >= 2 and len(token) < 26 and token not in english_stopwords and 'http' not in token and token not in stopwords_list.stopword_txt]
    text = nltk.Text(text_tokens)
    #print(text)
    fdist = FreqDist(text)
    fdist = fdist.most_common(30)
    #
    print(fdist)
    return fdist, text_tokens

def analyse_all(data):
    spec_chars = string.punctuation + '\n\xa0«»\t—…"<>?!.,;:'
    russian_stopwords = stopwords.words("russian")
    english_stopwords = stopwords.words("english")
    russian_stopwords.extend(['это','ну','но','еще','ещё','оно','типа'])
    text = str(data).lower().replace("'","").replace(",","").replace("[","").replace("]","").replace("-"," ")
    #print(text)
    text = remove_chars_from_text(text, spec_chars)
    text = remove_chars_from_text(text, string.digits)
    text_tokens = word_tokenize(text)
    #print(text_tokens)
    text_tokens = [token.strip() for token in text_tokens if token not in russian_stopwords and len(token) >= 2 and len(token) < 26 and token not in english_stopwords and 'http' not in token and token not in stopwords_list.stopword_txt]
    text = nltk.Text(text_tokens)
    fdist = FreqDist(data)
    fdist = fdist.most_common(30)
    #
    print(fdist)
    return fdist
