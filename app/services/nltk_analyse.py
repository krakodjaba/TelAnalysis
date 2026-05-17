import string
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from .utils import remove_chars_from_text, remove_emojis, read_conf, stopword_txt as stop_words

stemmer = SnowballStemmer("russian")

spec_chars = string.punctuation + '\n\xa0«»\t—…"<>?!.,;:꧁@#$%^&*()_-+=№%༺༺\\༺/༺-•'

# предзагруженные стоп-слова (nltk must be installed and stopwords downloaded)
try:
    russian_stopwords = set(stopwords.words("russian"))
except Exception:
    russian_stopwords = set()
russian_stopwords.update(['это', 'ну', 'но', 'еще', 'ещё', 'оно', 'типа'])
russian_stopwords.update(stop_words)
try:
    english_stopwords = set(stopwords.words("english"))
except Exception:
    english_stopwords = set()


def analyse(data, most_com):
    text = str(data).lower()
    # убираем системные действия — используй тот же список, что и раньше
    action_map = ['Invite Member', 'Kicked Members', 'Joined by Link', 'Pinned Message']
    for action in action_map:
        text = text.replace(action.lower(), "")
    text = remove_chars_from_text(text, spec_chars + string.digits)
    text = remove_emojis(text)

    if len(text) < 1:
        return [], []

    tokenizer = RegexpTokenizer(r'\w+')
    text_tokens = tokenizer.tokenize(text)

    if read_conf('select_type_stem') == 'On':
        text_tokens = [stemmer.stem(token) for token in text_tokens]

    text_tokens = [
        token for token in text_tokens
        if token not in russian_stopwords
        and token not in english_stopwords
        and 3 <= len(token) < 26
        and 'http' not in token
    ]

    fdist = FreqDist(text_tokens).most_common(most_com)
    return fdist, text_tokens


def analyse_all(data, most_com):
    text = str(data).lower()
    text = remove_chars_from_text(text, spec_chars + string.digits)
    text = remove_emojis(text)

    if len(text) < 1:
        return [], []

    tokenizer = RegexpTokenizer(r'\w+')
    text_tokens = tokenizer.tokenize(text)

    if read_conf('select_type_stem') == 'On':
        text_tokens = [stemmer.stem(token) for token in text_tokens]

    text_tokens = [
        token for token in text_tokens
        if token not in russian_stopwords
        and token not in english_stopwords
        and 4 <= len(token) < 26
        and 'http' not in token
    ]

    fdist = FreqDist(text_tokens).most_common(most_com)
    print(most_com, "\n", fdist)
    return fdist, [token for token, count in fdist]
