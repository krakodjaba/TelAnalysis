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
            if user:
                user = clear_user(user)
            if user not in users and user is not None:
                #user = str(user).replace(" ","").replace('"','').replace(".","").replace("꧁","")
                users.append(user)
                #put_code(user)
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
        if str(type(texts)) == "<class 'str'>":
            if texts != '':
                test = str(texts).replace("\\n","").replace("\n","").replace('"',"'",).strip()
                try:
                    exec('{}_list.append("{}")'.format(from_user, test))
                except Exception as ex:
                    put_code(ex, type(from_user),type(test), "2!")
                    continue
                count_messages +=1
        elif str(type(texts)) == "<class 'list'>":
            for textt in texts:
                try:
                    if len(textt['text']) >1:
                        test = textt['text']
                        #put_code(textt)
                        if "http" in test:
                            continue
                        else:
                            try:
                                test = test.replace("\\n","").replace("\n","").strip()
                            except:
                                put_code("pizda rulu")
                            try:
                                if test is None or test == "":
                                    continue
                                else:
                                    exec('{}_list.append("{}")'.format(from_user,str(test)))
                            except Exception as ex:
                                continue
                            count_messages +=1
                except Exception as ex:
                    try:
                        try:
                            test = textt.replace("\\n","").replace("\n","").strip()
                        except:
                            put_code("pizda rulu")
                        try:
                            if test is None or test == "":
                                continue
                            else:
                                exec('{}_list.append("{}")'.format(from_user,str(test)))
                        except Exception as ex:
                            continue
                        count_messages +=1
                    except:
                        put_code("vashe pizdqa")
    put_code('All used messages count:', count_messages)
    put_code('Messages from count users detected:', len(users))
    for i,user in enumerate(users):
        try:
            #exec('#print({}_list)'.format(user))
            exec('da = {}_list'.format(user))
            #print(da)

            genuy, tokens = nltk_analyse.analyse(da)
            for token in tokens:
                all_tokens.append(token)
            if len(da) >1:
                put_code("*"*90)
                put_code(f'--{i} {user}: ')
                for j,ga in enumerate(da):
                    put_code(f'[{j}] {ga}')
            else:
                put_code("continue")
                continue
            if len(genuy) >1:
                put_code(f"\nАнализ сообщений {user}:")
                for i in genuy:
                    try:
                        m = f'  {i[0]} - {i[1]}'
                        put_code(m)
                    except Exception as ex:
                        put_code(ex)
                        pass
                put_code("__")
            else:
                continue
        except Exception as ex:
            put_code(ex)
            continue
    all_tokens = nltk_analyse.analyse_all(all_tokens)
    put_code("\nАнализ Всего чата:")
    for i in all_tokens:
        try:
            m = m = f'  {i[0]} - {i[1]}'
            put_code(m)
        except Exception as ex:
            put_code(ex)
            pass
    put_code("__")
    put_button("Close",onclick=lambda: run_js('window.close()'), color='danger')
    put_button("Scroll Up",onclick=lambda: run_js('window.scrollTo(document.body.scrollHeight, 0)'))