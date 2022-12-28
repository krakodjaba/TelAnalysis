import re
import string
def clear_user(user):
    spec_chars = string.punctuation + '\n\xa0«»\t—…"<>?!.,;:꧁@#$%^&*()_-+=№%༺༺\༺/༺-•'
    user = str(user).replace(" ","").replace('"','').replace(".","").replace("꧁","")
    user = remove_chars_from_text(user, spec_chars)
    user = remove_emojis(user)
    return re.sub(r'[\x00-\x7f]', '', user)
    
def remove_chars_from_text(text, chars):
    return "".join([ch for ch in text if ch not in chars])

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        u"༺"
                        "]+", re.UNICODE)
    return re.sub(emoj, '', data)