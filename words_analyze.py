from utils import remove_chars_from_text, remove_emojis, clear_user
import nltk_analyse
import sys
from pywebio import input, config
from pywebio.output import put_html,put_text,put_image, put_button, put_code, clear, put_file
from pywebio.input import file_upload as file
from pywebio.session import run_js
import json, re, jmespath, string, collections
import networkx as nx
import matplotlib.pyplot as plt

config(theme='dark',title="TelAnalysis", description="Analysing Telegram CHATS-CHANNELS-GROUPS")
put_button("Scroll Down",onclick=lambda: run_js('window.scrollTo(0, document.body.scrollHeight)'))
put_html("<h1><center>Analyse of Telegram Chat<center></h1><br>")
put_button("Close",onclick=lambda: run_js('window.close()'), color='danger')
all_tokens = []
users = []
count_messages = 0
filename = sys.argv[1]
filename = filename.split(".")[0]
filename = filename.split("/")[1]
with open(f'asset/{filename}.json', 'r', encoding='utf-8') as datas:
    data = json.load(datas)
    sf = jmespath.search('messages[*]',data)
    for message in sf:
        try:
            user = jmespath.search('from', message)
            if user and user != '':
                user = clear_user(user)
                #print(user)
            if user not in users and user is not None:
                #user = str(user).replace(" ","").replace('"','').replace(".","").replace("꧁","")
                try:
                    user = user.replace(" ","")
                except:
                    put_text("error #9")
                #print(user)
                users.append(user)
                
                try:
                    exec('{}_list = []'.format(user))
                except Exception as ex:
                    put_code(ex, user)
                    continue
        except:
            continue
    for message in sf:
        texts = jmespath.search('text',message)
        from_user = jmespath.search('from', message)
        if from_user is None:
            continue
        else:
            from_user = clear_user(from_user)
            from_user = from_user.replace(" ","")
            #print(from_user)
        if str(type(texts)) == "<class 'str'>":
            if texts != '':
                test = str(texts).replace("\\n","").replace("\n","").strip()
                if "http" in test:
                    continue
                else:
                    try:
                        test = test.replace("\\n","").replace("\n","").replace('"',"'").strip()
                        
                        try:
                            test = remove_emojis(test)
                            
                        except:
                            test = test
                        
                    except:
                        put_text("error #1")
                    try:
                        if test is None or test == "":
                            continue
                        else:
                            exec('{}_list.append("{}")'.format(from_user,str(test)))
                            #print('{}_list.append("{}")'.format(from_user,str(test)))
                    except Exception as ex:
                        continue
                    count_messages +=1
        elif str(type(texts)) == "<class 'list'>":
            for textt in texts:
                try:
                    if len(textt['text']) >1:
                        test = textt['text']
                        
                        if "http" in test:
                            continue
                        else:
                            try:
                                test = test.replace("\\n","").replace("\n","").strip()
                                try:
                                    test = remove_emojis(test)
                                except:
                                    test = test
                            except:
                                put_text("error #2")
                            try:
                                if test is None or test == "":
                                    continue
                                else:
                                    exec('{}_list.append("{}")'.format(from_user,str(test)))
                                    #print('{}_list.append("{}")'.format(from_user,str(test)))
                            except Exception as ex:
                                continue
                            count_messages +=1
                except Exception as ex:
                    try:
                        try:
                            test = textt.replace("\\n","").replace("\n","").strip()
                            try:
                                test = remove_emojis(test)
                            except:
                                test = test
                        except:
                            put_text("error #3")
                        try:
                            if test is None or test == "":
                                continue
                            else:
                                exec('{}_list.append("{}")'.format(from_user,str(test)))
                                #print('{}_list.append("{}")'.format(from_user,str(test)))
                        except Exception as ex:
                            continue
                        count_messages +=1
                    except:
                        put_text("error #4")
    
    
    try:
        put_code(f'All used messages count: {count_messages}')
        put_code(f'Messages from count users detected: {len(users)}')
    except Exception as ex:
        put_text(ex)
    
    for i,user in enumerate(users):
        #print(users)
        try:
            try:
                if user and user != "":
                    put_text(f'Сообщения {user}:')
                    user = user.replace(" ","")
                    #user = user.split()
                    #print(user)
                    exec('da = {}_list'.format(user))
                    genuy, tokens = nltk_analyse.analyse(da)
                    for token in tokens:
                        all_tokens.append(token)
                    if len(da) >=1:
                        #put_code("*"*90)
                        put_code(f'--{i} {user}: ')
                        for j,ga in enumerate(da):
                            put_code(f'[{j}] {ga}')
                    else:
                        #print(da)
                        continue
                    if len(genuy) >=1:
                        put_text(f"\nАнализ сообщений {user}:")
                        for i in genuy:
                            try:
                                m = f'  {i[0]} - {i[1]}'
                                put_code(m)
                            except Exception as ex:
                                put_text(f"error #5 {ex}")
                                pass
                        put_text("__"*45)
                    else:
                        continue
            except Exception as ex:
                put_text(f"[{user}] error #8 {ex}")
        except Exception as ex:
            put_text(f'{ex} error #6')
            continue
    all_tokens = nltk_analyse.analyse_all(all_tokens)
    put_text("\nАнализ Всего чата:")
    for i in all_tokens:
        try:
            m = m = f'  {i[0]} - {i[1]}'
            put_code(m)
        except Exception as ex:
            put_text(f"error #7 {ex}")
            pass
    put_text("__"*45)
    put_button("Close",onclick=lambda: run_js('window.close()'), color='danger')
    put_button("Scroll Up",onclick=lambda: run_js('window.scrollTo(document.body.scrollHeight, 0)'))