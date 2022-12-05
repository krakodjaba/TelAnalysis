import json
import jmespath
from utils import remove_chars_from_text
import nltk_analyse
import string

all_tokens = []
users = []
count_messages = 0
filename = input('filename: ')
with open(filename, 'r', encoding='utf-8') as datas:
    data = json.load(datas)
    sf = jmespath.search('messages[*]',data)
    for message in sf:
        spec_chars = string.punctuation + '\n\xa0«»\t—…"<>?!.,;:'
        try:
            user = jmespath.search('from', message)
            print(user)
            user = remove_chars_from_text(user, spec_chars)
            user = remove_chars_from_text(user, string.digits)
            if user is not None:
                user = str(user).replace(" ","").replace('"','').replace(".","").replace("꧁","")
            if user not in users and user is not None:
                #user = str(user).replace(" ","").replace('"','').replace(".","").replace("꧁","")
                users.append(user)
                print(user)
                try:
                    exec('{}_list = []'.format(user))
                except Exception as ex:
                    print(ex)
                    pass
        except:
            continue
    #print(users)
    for message in sf:
        texts = jmespath.search('text',message)
        from_user = jmespath.search('from', message)
        if from_user is None:
            continue
        else:
            from_user = from_user.replace(" ","").replace('"','').replace(".","").replace("꧁","")
        if str(type(texts)) == "<class 'str'>":
            if texts != '':
                test = texts.replace("\\n","").replace("\n","").replace('"',"'",).strip()
                try:
                    exec('{}_list.append("{}")'.format(from_user,test))
                except Exception as ex:
                    print(ex)
                    continue
                #print(texts.replace("\\n","").replace("\n","").strip())
                count_messages +=1
        elif str(type(texts)) == "<class 'list'>":
            for text in texts:
                try:
                    if len(text['text']) >1:
                        test = text['text'].replace("\\n","").replace("\n","").strip()
                        try:
                            exec('{}_list.append("{}")'.format(from_user,test))
                        except Exception as ex:
                            continue
                        #print(text['text'].replace("\\n","").replace("\n","").strip())
                        count_messages +=1
                except Exception as ex:
                    print(ex)
                    pass
    print('All used messages count:', count_messages)
    print('Messages from count users detected:', len(users))
    for i,user in enumerate(users):
        try:
            exec('da = {}_list'.format(user))
            genuy, tokens = nltk_analyse.analyse(da)
            for token in tokens:
                all_tokens.append(token)
            if len(da) >1:
                print("*"*90)
                print(f'--{i} {user}: ')
                for j,ga in enumerate(da):
                    print(f'[{j}] {ga}')
            else:
                continue
            if len(genuy) >1:
                print(f"\nАнализ сообщений {user}:")
                for i in genuy:
                    try:
                        print('  ',i[0], "-", i[1])
                    except Exception as ex:
                        print(ex)
                        pass
                print("__")
            else:
                continue
        except Exception as ex:
            print(ex)
            continue
    all_tokens = nltk_analyse.analyse_all(all_tokens)
    print("\nАнализ Всего чата:")
    for i in all_tokens:
        try:
            print('  ',i[0], "-", i[1])
        except Exception as ex:
            print(ex)
            pass
    print("__")