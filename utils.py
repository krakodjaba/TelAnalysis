import re
import string
import emoji
import os
import subprocess
import platform
import json, jmespath, requests
from pywebio.output import put_html,toast,put_text,put_image,put_collapse, put_button, put_code, clear, put_file, popup, put_table
spec_chars = string.punctuation + '\n\xa0«»\t—…"<>?!.,;:꧁@#$%^&*()_+=№%༺༺\༺/༺•'

##config telanalysis
def read_conf(option):
    try:
        with open('config.json', 'r') as read_conf:
            read_conf = json.load(read_conf)
            select_type_stem = jmespath.search(f'{option}',read_conf)
        return select_type_stem
    except:
        write_conf('{"select_type_stem": "Off", "most_com": 30, "most_com_channel":100}')

def write_conf(dct):
    with open('config.json', 'w') as fw:
        json.dump(dct, fw)

def clear_console():
    system = platform.system()
    if system == 'Windows':
        subprocess.run('cls', shell=True)
    elif system == 'Darwin' or system == 'Linux':
        subprocess.run('clear', shell=True)
        
def open_url():
    system = platform.system()
    if system == 'Windows':
        subprocess.run(f'start http://127.0.0.1:9993', shell=True)
    elif system == 'Darwin' or system == 'Linux':
        subprocess.run('open http://127.0.0.1:9993', shell=True)

def remove_chars_from_text(text, char=None):
    if char is None:
        char = spec_chars
    
    # Используем регулярное выражение для замены нежелательных символов на пробелы
    pattern = f"[{re.escape(char)}]"
    text = re.sub(pattern, ' ', text)  # Заменяем спецсимволы на пробелы
    text = re.sub(r'\s+', ' ', text).strip()  # Удаляем лишние пробелы
    return text

    toast(content='Wait Result..',duration=0)
    phonenumbers = []
    ids = []
    telegram_ids = []
    firstnames = []
    surnames = []
    emails = []
    trades = []
    social_medias = []
    addresses = []
    technicals_data = []
    tg_id = int(tg_id.replace("user","").replace("channel","").strip())
    if tg_id:
        #print(int(tg_id))
        req = requests.post(f'https://osintframework.ru/api/telegram/telegram-user-somevendor', json={"telegram_id": int(tg_id)},
                                headers={"Authorization": token},
                                timeout=60)
        try:
            finded_data = req.json()["telegram_id_somevendor"]["finded_data"]
        except:
            print('error')
            print(req)
            raise
        if len(finded_data) == 0:
            toast(content="Can't find result.",duration=1)
            pass
        else:
            if finded_data:
                #print(finded_data)
                for i in finded_data:
                    for j in i:
                        if 'phone_number' in j:
                            phonenumber = i[j]
                            if phonenumber not in phonenumbers:
                                phonenumbers.append(phonenumber)
                        phonenumberss = '\n'.join(phonenumbers)
                        if 'id' in j:
                            id = i[j]
                            if id not in ids:
                                ids.append(id)
                        try:
                            idss = '\n'.join(ids)
                        except:
                            idss = ids
                        if 'telegram_id' in j:
                            telegram_id = i[j]
                            if telegram_id not in telegram_ids:
                                telegram_ids.append(telegram_id)
                        try:
                            telegram_idss = '\n'.join(telegram_ids)
                        except:
                            telegram_idss = telegram_ids
                        if 'firstname' in j:
                            firstname = i[j]
                            if firstname not in firstnames:
                                firstnames.append(firstname)
                        firstnamess = '\n'.join(firstnames)
                        if 'surname' in j:
                            surname = i[j]
                            if surname not in surnames:
                                surnames.append(surname)
                        surnamess = '\n'.join(surnames)
                        if 'email' in j:
                            email = i[j]
                            if email not in emails:
                                emails.append(email)
                        emailss = '\n'.join(emails)
                        if 'trade' in j:
                            trade = i[j]
                            if trade not in trades:
                                trades.append(trade)
                        tradess = '\n'.join(trades)
                        if 'social_media' in j:
                            social_media = i[j]
                            if social_media not in social_medias:
                                social_medias.append(social_media)
                        social_mediass = '\n'.join(social_medias)
                        if 'address' in j:
                            address = i[j]
                            if address not in addresses:
                                addresses.append(address)
                        addressess = '\n'.join(addresses)
                        if 'technical_data' in j:
                            technical_data = i[j]
                            if technical_data not in technicals_data:
                                technicals_data.append(technical_data)
                        technicals_datas = '\n'.join(technicals_data)
            tg_data = []
            tg_data.append([phonenumbers, telegram_ids, firstnames, emails, addresses,trades, social_medias, technicals_datas])
            data = f"""
        PhoneNumber: {phonenumbers}
        Telegram: {telegram_ids}
        surname: {surnames}
        firstname: {firstnames}
        email: {emails}
        address: {addresses}
        trade: {trades}
        social_media: {social_medias}
        techincal_data: {technicals_data}
            """
            popup('Telegram INFO', [
    put_html(f'<h3>Telegram ID:{telegram_ids}</h3>'),
    put_table(tg_data, header=['PhoneNumber', 'Telegram', 'Firstname','Email', 'Address',
    'Trades','Social_media','Technicals Data'])
])

def remove_emojis(data):
    
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002500-\U00002BEF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\U00002700-\U000027BF"
        u"\U00002600-\U000026FF"
        u"\U0001F900-\U0001F9FF"
        u"\U0001FA70-\U0001FAFF"
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
        u"\ufe0f"
        u"\u3030"
        u"\u231A-\u231B"
        u"\u23E9-\u23EC"
        u"\u25FD-\u25FE"
        u"\u2614-\u2615"
        u"\u2648-\u2653"
        u"\u26AA-\u26AB"
        u"\u26BD-\u26BE"
        u"\u26C4-\u26C5"
        u"\u26F2-\u26F3"
        u"\u270A-\u270B"
        u"\u2753-\u2755"
        u"\u2795-\u2797"
        u"\u2B1B-\u2B1C"
        u"\U0001F191-\U0001F19A"
        u"\U0001F232-\U0001F236"
        u"\U0001F238-\U0001F23A"
        u"\U0001F250-\U0001F251"
        u"\U0001F300-\U0001F30C"
        u"\U0001F30D-\U0001F30E"
        u"\U0001F313-\U0001F315"
        u"\U0001F316-\U0001F318"
        u"\U0001F31D-\U0001F31E"
        u"\U0001F31F-\U0001F320"
        u"\U0001F32D-\U0001F32F"
        u"\U0001F330-\U0001F331"
        u"\U0001F332-\U0001F333"
        u"\U0001F334-\U0001F335"
        u"\U0001F337-\U0001F34A"
        u"\U0001F34C-\U0001F34F"
        u"\U0001F351-\U0001F37B"
        u"\U0001F37E-\U0001F37F"
        u"\U0001F380-\U0001F393"
        u"\U0001F3A0-\U0001F3C4"
        u"\U0001F3CF-\U0001F3D3"
        u"\U0001F3E0-\U0001F3E3"
        u"\U0001F3E5-\U0001F3F0"
        u"\U0001F3F8-\U0001F407"
        u"\U0001F409-\U0001F40B"
        u"\U0001F40C-\U0001F40E"
        u"\U0001F40F-\U0001F410"
        u"\U0001F411-\U0001F412"
        u"\U0001F417-\U0001F429"
        u"\U0001F42B-\U0001F43E"
        u"\U0001F442-\U0001F464"
        u"\U0001F466-\U0001F46B"
        u"\U0001F46C-\U0001F46D"
        u"\U0001F46E-\U0001F4AC"
        u"\U0001F4AE-\U0001F4B5"
        u"\U0001F4B6-\U0001F4B7"
        u"\U0001F4B8-\U0001F4EB"
        u"\U0001F4EC-\U0001F4ED"
        u"\U0001F4F0-\U0001F4F4"
        u"\U0001F4F6-\U0001F4F7"
        u"\U0001F4F9-\U0001F4FC"
        u"\U0001F4FF-\U0001F502"
        u"\U0001F504-\U0001F507"
        u"\U0001F50A-\U0001F514"
        u"\U0001F516-\U0001F52B"
        u"\U0001F52C-\U0001F52D"
        u"\U0001F52E-\U0001F53D"
        u"\U0001F54B-\U0001F54E"
        u"\U0001F550-\U0001F55B"
        u"\U0001F55C-\U0001F567"
        u"\U0001F595-\U0001F596"
        u"\U0001F5FB-\U0001F5FF"
        u"\U0001F601-\U0001F606"
        u"\U0001F607-\U0001F608"
        u"\U0001F609-\U0001F60D"
        u"\U0001F612-\U0001F614"
        u"\U0001F61C-\U0001F61E"
        u"\U0001F620-\U0001F625"
        u"\U0001F626-\U0001F627"
        u"\U0001F628-\U0001F62B"
        u"\U0001F62E-\U0001F62F"
        u"\U0001F630-\U0001F633"
        u"\U0001F637-\U0001F640"
        u"\U0001F641-\U0001F644"
        u"\U0001F645-\U0001F64F"
        u"\U0001F681-\U0001F682"
        u"\U0001F683-\U0001F685"
        u"\U0001F68A-\U0001F68B"
        u"\U0001F691-\U0001F693"
        u"\U0001F699-\U0001F69A"
        u"\U0001F69B-\U0001F6A1"
        u"\U0001F6A4-\U0001F6A5"
        u"\U0001F6A7-\U0001F6AD"
        u"\U0001F6AE-\U0001F6B1"
        u"\U0001F6B3-\U0001F6B5"
        u"\U0001F6B7-\U0001F6B8"
        u"\U0001F6B9-\U0001F6BE"
        u"\U0001F6C1-\U0001F6C5"
        u"\U0001F6D1-\U0001F6D2"
        u"\U0001F6D6-\U0001F6D7"
        u"\U0001F6DD-\U0001F6DF"
        u"\U0001F6EB-\U0001F6EC"
        u"\U0001F6F4-\U0001F6F6"
        u"\U0001F6F7-\U0001F6F8"
        u"\U0001F6FB-\U0001F6FC"
        u"\U0001F7E0-\U0001F7EB"
        u"\U0001F90D-\U0001F90F"
        u"\U0001F910-\U0001F918"
        u"\U0001F919-\U0001F91E"
        u"\U0001F920-\U0001F927"
        u"\U0001F928-\U0001F92F"
        u"\U0001F931-\U0001F932"
        u"\U0001F933-\U0001F93A"
        u"\U0001F93C-\U0001F93E"
        u"\U0001F940-\U0001F945"
        u"\U0001F947-\U0001F94B"
        u"\U0001F94D-\U0001F94F"
        u"\U0001F950-\U0001F95E"
        u"\U0001F95F-\U0001F96B"
        u"\U0001F96C-\U0001F970"
        u"\U0001F973-\U0001F976"
        u"\U0001F977-\U0001F978"
        u"\U0001F97C-\U0001F97F"
        u"\U0001F980-\U0001F984"
        u"\U0001F985-\U0001F991"
        u"\U0001F992-\U0001F997"
        u"\U0001F998-\U0001F9A2"
        u"\U0001F9A3-\U0001F9A4"
        u"\U0001F9A5-\U0001F9AA"
        u"\U0001F9AB-\U0001F9AD"
        u"\U0001F9AE-\U0001F9AF"
        u"\U0001F9B0-\U0001F9B9"
        u"\U0001F9BA-\U0001F9BF"
        u"\U0001F9C1-\U0001F9C2"
        u"\U0001F9C3-\U0001F9CA"
        u"\U0001F9CD-\U0001F9CF"
        u"\U0001F9D0-\U0001F9E6"
        u"\U0001F9E7-\U0001F9FF"
        u"\U0001FA70-\U0001FA73"
        u"\U0001FA78-\U0001FA7A"
        u"\U0001FA7B-\U0001FA7C"
        u"\U0001FA80-\U0001FA82"
        u"\U0001FA83-\U0001FA86"
        u"\U0001FA90-\U0001FA95"
        u"\U0001FA96-\U0001FAA8"
        u"\U0001FAA9-\U0001FAAC"
        u"\U0001FAB0-\U0001FAB6"
        u"\U0001FAB7-\U0001FABA"
        u"\U0001FAC0-\U0001FAC2"
        u"\U0001FAC3-\U0001FAC5"
        u"\U0001FAD0-\U0001FAD6"
        u"\U0001FAD7-\U0001FAD9"
        u"\U0001FAE0-\U0001FAE7"
        u"\U0001FAF0-\U0001FAF6"
        u"\u23F0"
        u"\u23F3"
        u"\u267F"
        u"\u2693"
        u"\u26A1"
        u"\u26CE"
        u"\u26D4"
        u"\u26EA"
        u"\u26F5"
        u"\u26FA"
        u"\u26FD"
        u"\u2705"
        u"\u2728"
        u"\u274C"
        u"\u274E"
        u"\u2757"
        u"\u27B0"
        u"\u27BF"
        u"\u2B50"
        u"\u2B55"
        u"\U0001F004"
        u"\U0001F0CF"
        u"\U0001F18E"
        u"\U0001F201"
        u"\U0001F21A"
        u"\U0001F22F"
        u"\U0001F30F"
        u"\U0001F310"
        u"\U0001F311"
        u"\U0001F312"
        u"\U0001F319"
        u"\U0001F31A"
        u"\U0001F31B"
        u"\U0001F31C"
        u"\U0001F34B"
        u"\U0001F350"
        u"\U0001F37C"
        u"\U0001F3C5"
        u"\U0001F3C6"
        u"\U0001F3C7"
        u"\U0001F3C8"
        u"\U0001F3C9"
        u"\U0001F3CA"
        u"\U0001F3E4"
        u"\U0001F3F4"
        u"\U0001F408"
        u"\U0001F413"
        u"\U0001F414"
        u"\U0001F415"
        u"\U0001F416"
        u"\U0001F42A"
        u"\U0001F440"
        u"\U0001F465"
        u"\U0001F4AD"
        u"\U0001F4EE"
        u"\U0001F4EF"
        u"\U0001F4F5"
        u"\U0001F4F8"
        u"\U0001F503"
        u"\U0001F508"
        u"\U0001F509"
        u"\U0001F515"
        u"\U0001F57A"
        u"\U0001F5A4"
        u"\U0001F600"
        u"\U0001F60E"
        u"\U0001F60F"
        u"\U0001F610"
        u"\U0001F611"
        u"\U0001F615"
        u"\U0001F616"
        u"\U0001F617"
        u"\U0001F618"
        u"\U0001F619"
        u"\U0001F61A"
        u"\U0001F61B"
        u"\U0001F61F"
        u"\U0001F62C"
        u"\U0001F62D"
        u"\U0001F634"
        u"\U0001F635"
        u"\U0001F636"
        u"\U0001F680"
        u"\U0001F686"
        u"\U0001F687"
        u"\U0001F688"
        u"\U0001F689"
        u"\U0001F68C"
        u"\U0001F68D"
        u"\U0001F68E"
        u"\U0001F68F"
        u"\U0001F690"
        u"\U0001F694"
        u"\U0001F695"
        u"\U0001F696"
        u"\U0001F697"
        u"\U0001F698"
        u"\U0001F6A2"
        u"\U0001F6A3"
        u"\U0001F6A6"
        u"\U0001F6B2"
        u"\U0001F6B6"
        u"\U0001F6BF"
        u"\U0001F6C0"
        u"\U0001F6CC"
        u"\U0001F6D0"
        u"\U0001F6D5"
        u"\U0001F6F9"
        u"\U0001F6FA"
        u"\U0001F7F0"
        u"\U0001F90C"
        u"\U0001F91F"
        u"\U0001F930"
        u"\U0001F93F"
        u"\U0001F94C"
        u"\U0001F971"
        u"\U0001F972"
        u"\U0001F979"
        u"\U0001F97A"
        u"\U0001F97B"
        u"\U0001F9C0"
        u"\U0001F9CB"
        u"\U0001F9CC"
        u"\U0001FA74"
        u"\u00A9"
        u"\uFE0F"
        u"\u00AE"
        u"\u203C"
        u"\u2049"
        u"\u2122"
        u"\u2139"
        u"\u2194"
        u"\u2195"
        u"\u2196"
        u"\u2197"
        u"\u2198"
        u"\u2199"
        u"\u21A9"
        u"\u21AA"
        u"\u23CF"
        u"\u23ED"
        u"\u23EE"
        u"\u23EF"
        u"\u23F1"
        u"\u23F2"
        u"\u23F8"
        u"\u23F9"
        u"\u23FA"
        u"\u24C2"
        u"\u25AA"
        u"\u25AB"
        u"\u25B6"
        u"\u25C0"
        u"\u25FB"
        u"\u25FC"
        u"\u2600"
        u"\u2601"
        u"\u2602"
        u"\u2603"
        u"\u2604"
        u"\u260E"
        u"\u2611"
        u"\u2618"
        u"\u261D"
        u"\u2620"
        u"\u2622"
        u"\u2623"
        u"\u2626"
        u"\u262A"
        u"\u262E"
        u"\u262F"
        u"\u2638"
        u"\u2639"
        u"\u263A"
        u"\u2640"
        u"\u2642"
        u"\u265F"
        u"\u2660"
        u"\u2663"
        u"\u2665"
        u"\u2666"
        u"\u2668"
        u"\u267B"
        u"\u267E"
        u"\u2692"
        u"\u2694"
        u"\u2695"
        u"\u2696"
        u"\u2697"
        u"\u2699"
        u"\u269B"
        u"\u269C"
        u"\u26A0"
        u"\u26A7"
        u"\u26B0"
        u"\u26B1"
        u"\u26C8"
        u"\u26CF"
        u"\u26D1"
        u"\u26D3"
        u"\u26E9"
        u"\u26F0"
        u"\u26F1"
        u"\u26F4"
        u"\u26F7"
        u"\u26F8"
        u"\u26F9"
        u"\u2702"
        u"\u2708"
        u"\u2709"
        u"\u270C"
        u"\u270D"
        u"\u270F"
        u"\u2712"
        u"\u2714"
        u"\u2716"
        u"\u271D"
        u"\u2721"
        u"\u2733"
        u"\u2734"
        u"\u2744"
        u"\u2747"
        u"\u2763"
        u"\u2764"
        u"\u27A1"
        u"\u2934"
        u"\u2935"
        u"\u2B05"
        u"\u2B06"
        u"\u2B07"
        u"\u303D"
        u"\u3297"
        u"\u3299"
        u"\U0001F170"
        u"\U0001F171"
        u"\U0001F17E"
        u"\U0001F17F"
        u"\U0001F202"
        u"\U0001F237"
        u"\U0001F321"
        u"\U0001F324"
        u"\U0001F325"
        u"\U0001F326"
        u"\U0001F327"
        u"\U0001F328"
        u"\U0001F329"
        u"\U0001F32A"
        u"\U0001F32B"
        u"\U0001F32C"
        u"\U0001F336"
        u"\U0001F37D"
        u"\U0001F396"
        u"\U0001F397"
        u"\U0001F399"
        u"\U0001F39A"
        u"\U0001F39B"
        u"\U0001F39E"
        u"\U0001F39F"
        u"\U0001F3CB"
        u"\U0001F3CC"
        u"\U0001F3CD"
        u"\U0001F3CE"
        u"\U0001F3D4"
        u"\U0001F3D5"
        u"\U0001F3D6"
        u"\U0001F3D7"
        u"\U0001F3D8"
        u"\U0001F3D9"
        u"\U0001F3DA"
        u"\U0001F3DB"
        u"\U0001F3DC"
        u"\U0001F3DD"
        u"\U0001F3DE"
        u"\U0001F3DF"
        u"\U0001F3F3"
        u"\U0001F3F5"
        u"\U0001F3F7"
        u"\U0001F43F"
        u"\U0001F441"
        u"\U0001F4FD"
        u"\U0001F549"
        u"\U0001F54A"
        u"\U0001F56F"
        u"\U0001F570"
        u"\U0001F573"
        u"\U0001F574"
        u"\U0001F575"
        u"\U0001F576"
        u"\U0001F577"
        u"\U0001F578"
        u"\U0001F579"
        u"\U0001F587"
        u"\U0001F58A"
        u"\U0001F58B"
        u"\U0001F58C"
        u"\U0001F58D"
        u"\U0001F590"
        u"\U0001F5A5"
        u"\U0001F5A8"
        u"\U0001F5B1"
        u"\U0001F5B2"
        u"\U0001F5BC"
        u"\U0001F5C2"
        u"\U0001F5C3"
        u"\U0001F5C4"
        u"\U0001F5D1"
        u"\U0001F5D2"
        u"\U0001F5D3"
        u"\U0001F5DC"
        u"\U0001F5DD"
        u"\U0001F5DE"
        u"\U0001F5E1"
        u"\U0001F5E3"
        u"\U0001F5E8"
        u"\U0001F5EF"
        u"\U0001F5F3"
        u"\U0001F5FA"
        u"\U0001F6CB"
        u"\U0001F6CD"
        u"\U0001F6CE"
        u"\U0001F6CF"
        u"\U0001F6E0"
        u"\U0001F6E1"
        u"\U0001F6E2"
        u"\U0001F6E3"
        u"\U0001F6E4"
        u"\U0001F6E5"
        u"\U0001F6E9"
        u"\U0001F6F0"
        u"\U0001F6F3"
        u"\u0023"
        u"\u20E3"
        u"\u002A"
        u"\u0030"
        u"\u0031"
        u"\u0032"
        u"\u0033"
        u"\u0034"
        u"\u0035"
        u"\u0036"
        u"\u0037"
        u"\u0038"
        u"\u0039"
        u"\U0001F1E6"
        u"\U0001F1E8"
        u"\U0001F1E9"
        u"\U0001F1EA"
        u"\U0001F1EB"
        u"\U0001F1EC"
        u"\U0001F1EE"
        u"\U0001F1F1"
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F1F6"
        u"\U0001F1F7"
        u"\U0001F1F8"
        u"\U0001F1F9"
        u"\U0001F1FA"
        u"\U0001F1FC"
        u"\U0001F1FD"
        u"\U0001F1FF"
        u"\U0001F1E7"
        u"\U0001F1ED"
        u"\U0001F1EF"
        u"\U0001F1F3"
        u"\U0001F1FB"
        u"\U0001F1FE"
        u"\U0001F1F0"
        u"\U0001F1F5"
        u"\U000E0067"
        u"\U000E0062"
        u"\U000E0065"
        u"\U000E006E"
        u"\U000E007F"
        u"\U000E0073"
        u"\U000E0063"
        u"\U000E0074"
        u"\U000E0077"
        u"\U000E006C"
        u"\U0001F3FB"
        u"\U0001F3FC"
        u"\U0001F3FD"
        u"\U0001F3FE"
        u"\U0001F3FF"
        u"\u270A"
        u"\u270B"
        u"\U0001F385"
        u"\U0001F3C2"
        u"\U0001F3C3"
        u"\U0001F3C4"
        u"\U0001F442"
        u"\U0001F443"
        u"\U0001F446"
        u"\U0001F447"
        u"\U0001F448"
        u"\U0001F449"
        u"\U0001F44A"
        u"\U0001F44B"
        u"\U0001F44C"
        u"\U0001F44D"
        u"\U0001F44E"
        u"\U0001F44F"
        u"\U0001F450"
        u"\U0001F466"
        u"\U0001F467"
        u"\U0001F468"
        u"\U0001F469"
        u"\U0001F46B"
        u"\U0001F46C"
        u"\U0001F46D"
        u"\U0001F46E"
        u"\U0001F470"
        u"\U0001F471"
        u"\U0001F472"
        u"\U0001F473"
        u"\U0001F474"
        u"\U0001F475"
        u"\U0001F476"
        u"\U0001F477"
        u"\U0001F478"
        u"\U0001F47C"
        u"\U0001F481"
        u"\U0001F482"
        u"\U0001F483"
        u"\U0001F485"
        u"\U0001F486"
        u"\U0001F487"
        u"\U0001F48F"
        u"\U0001F491"
        u"\U0001F4AA"
        u"\U0001F595"
        u"\U0001F596"
        u"\U0001F645"
        u"\U0001F646"
        u"\U0001F647"
        u"\U0001F64B"
        u"\U0001F64C"
        u"\U0001F64D"
        u"\U0001F64E"
        u"\U0001F64F"
        u"\U0001F6B4"
        u"\U0001F6B5"
        u"\U0001F90F"
        u"\U0001F918"
        u"\U0001F919"
        u"\U0001F91A"
        u"\U0001F91B"
        u"\U0001F91C"
        u"\U0001F91D"
        u"\U0001F91E"
        u"\U0001F926"
        u"\U0001F931"
        u"\U0001F932"
        u"\U0001F933"
        u"\U0001F934"
        u"\U0001F935"
        u"\U0001F936"
        u"\U0001F937"
        u"\U0001F938"
        u"\U0001F939"
        u"\U0001F93D"
        u"\U0001F93E"
        u"\U0001F977"
        u"\U0001F9B5"
        u"\U0001F9B6"
        u"\U0001F9B8"
        u"\U0001F9B9"
        u"\U0001F9BB"
        u"\U0001F9CD"
        u"\U0001F9CE"
        u"\U0001F9CF"
        u"\U0001F9D1"
        u"\U0001F9D2"
        u"\U0001F9D3"
        u"\U0001F9D4"
        u"\U0001F9D5"
        u"\U0001F9D6"
        u"\U0001F9D7"
        u"\U0001F9D8"
        u"\U0001F9D9"
        u"\U0001F9DA"
        u"\U0001F9DB"
        u"\U0001F9DC"
        u"\U0001F9DD"
        u"\U0001FAC3"
        u"\U0001FAC4"
        u"\U0001FAC5"
        u"\U0001FAF0"
        u"\U0001FAF1"
        u"\U0001FAF2"
        u"\U0001FAF3"
        u"\U0001FAF4"
        u"\U0001FAF5"
        u"\U0001FAF6"
        u"\u0e4b"
        u"\u0489"
        u"\u0338"
        u"\u1D11E"
        u"\u035E"
        u"\u1F132"
        u"\uA9C2"
        u"\u0335"
        u"\u00AD"
        u"\u10121"
        u"\u00BF"
        u"\u1F153"
                        "]+", re.UNICODE)
    emoj = re.compile(r'(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])')
    data = re.sub(emoj, '', data)
    spec_chars = string.punctuation + '\n\xa0«»\t—…"<>?!.,;:꧁@#$%^&*()_+=№%༺༺\༺/༺•'
    data = remove_chars_from_text(data, spec_chars)
    data = re.sub(r'[\x00-\x7f]', ' ', data)
    data = data.replace("  "," ").strip()
    try:
        #print(data)
        data = emoji.demojize(data)
        #print(data)
        data = str(data.split(":")[0])
        #print(data)
    except:
        data = data
    return str(data).replace("[","").replace("]","").replace("'","").replace("  ","").replace(",","")

def clear_user(user):
    # Убираем спецсимволы, эмодзи и очищаем текст
    user = str(user).replace(" ", "").replace('"', '').replace(".", "").replace("꧁", "")
    user = remove_chars_from_text(user)
    user = remove_emojis(user)
    
    return user.strip()  # Удаляем пробелы в начале и конце строки