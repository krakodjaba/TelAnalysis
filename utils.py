import re
import string

spec_chars = string.punctuation + '\n\xa0«»\t—…"<>?!.,;:꧁@#$%^&*()_-+=№%༺༺\༺/༺-•'
    
def remove_chars_from_text(text, char=None):
    if char:
        char = char
    else:
        char = spec_chars
    text = "".join([ch for ch in text if ch not in char])
    #text = text.replace("  "," ")
    return text 
    
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
        u"\U00002700-\U000027BF"  # Dingbats
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U00002600-\U000026FF"  # Miscellaneous Symbols
        u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols And Pictographs
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\u180b"
        u"\u180c"
        u"\u0489"
        u"\u2019"
        u"\u00A4"
        u"\u035c"
        u"\u2328"
        u"\ufe0f"  # dingbats
        u"\u3030"
                        "]+", re.UNICODE)
    data = re.sub(emoj, '', data)
    spec_chars = string.punctuation + '\n\xa0«»\t—…"<>?!.,;:꧁@#$%^&*()_-+=№%༺༺\༺/༺-•'
    data = remove_chars_from_text(data, spec_chars)
    data = re.sub(r'[\x00-\x7f]', ' ', data)
    data = data.replace("  "," ").split()
    return str(data).replace("[","").replace("]","").replace("'","").replace("  ","").replace(",","")

def clear_user(user):
    spec_chars = string.punctuation + '\n\xa0«»\t—…"<>?!.,;:꧁@#$%^&*()_-+=№%༺༺\༺/༺-•'
    user = str(user).replace(" ","").replace('"','').replace(".","").replace("꧁","").replace(spec_chars, "")
    user = remove_chars_from_text(user)
    user = remove_emojis(user)
    
    #user = re.sub(r'[\x00-\x7f]', ' ', user)
    return str(user).replace("[","").replace("]","").replace("'","")