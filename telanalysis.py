#Telanalysis by Eduard Isaev @e_isaevsan

from pywebio import start_server, input, config
from pywebio.output import put_html,put_text,put_image, put_button,put_table, put_collapse, put_code, clear, put_file,Output, toast
from pywebio.input import file_upload as file
from pywebio.session import run_js
from pywebio.input import select, slider
import json, re, jmespath, string, collections, time
from utils import remove_chars_from_text, remove_emojis, clear_user, clear_console, read_conf, write_conf,open_url
import nltk_analyse, channel_analyse
import networkx as nx
import matplotlib.pyplot as plt
import sys
import matplotlib
matplotlib.use('Agg')

global select_type_stem


## config pywebio
config(theme='dark',title="TelAnalysis", description="Analysing Telegram CHATS-CHANNELS-GROUPS")


def generator(filename):
    import collections  # Импортируем здесь, если используется в функции
    import networkx as nx
    import matplotlib.pyplot as plt

    tables = []
    clear_console()
    filename = filename.split(".")[0]
    filename = filename.split("/")[1]
    dates_list = []
    names = []
    
    open(f'asset/edges_{filename}.csv', 'w', encoding='utf-8').write("source,target,label")
    
    with open(f'asset/{filename}.json', 'r', encoding='utf-8') as f:
        jsondata = json.load(f)
        group_name = jmespath.search('name', jsondata)
        put_html(f"<center><h1>{group_name}</h1><center>")
        sf = jmespath.search('messages[*]', jsondata)
        toast(content='Wait Result..', duration=0)
        
        for message in sf:
            fromm = jmespath.search('from', message)
            if fromm is None:
                continue
            from_id = jmespath.search('from_id', message)
            date = jmespath.search('date', message)
            dates_list.append(date)
            
            if from_id in ['source', 'target', None]:
                continue
            
            name_id = f'{fromm}, {from_id}'
            names.append(name_id)
            
            text_message = jmespath.search('text', message)
            if isinstance(text_message, list):
                for textt in message:
                    try:
                        if isinstance(textt, dict) and 'text' in textt:  # Проверяем, что textt - словарь, и у него есть ключ 'text'
                            test = textt['text']
                        elif isinstance(textt, str):  # Если это строка, обрабатываем ее как есть
                            test = textt
                        else:
                            continue

                        test = test.replace("\\n", "").replace("\n", "").strip()
                        try:
                            message_clean = remove_emojis(test)
                        except:
                            message_clean = test
                    except Exception as ex:
                        print(f"Error: {ex}")
                        continue

            else:
                try:
                    message_clean = remove_emojis(text_message)
                except:
                    message_clean = text_message

            if not message_clean:
                continue
            
            reply_to_message_id = jmespath.search('reply_to_message_id', message)
            if reply_to_message_id:
                for reply_message in sf:
                    message_id = jmespath.search('id', reply_message)
                    if reply_to_message_id == message_id:
                        reply_to = jmespath.search('from', reply_message)
                        reply_to_id = jmespath.search('from_id', reply_message)
                        reply_name_id = f'{reply_to}, {reply_to_id}'
                        names.append(reply_name_id)
                        try:
                            open(f'asset/edges_{filename}.csv', 'a', encoding='utf-8').write(f'\n{from_id},{reply_to_id},{fromm}-{reply_to}')
                        except Exception as ex:
                            print(ex)
                            pass
            else:
                try:
                    open(f'asset/edges_{filename}.csv', 'a', encoding='utf-8').write(f'\n{from_id},{from_id},{fromm}')
                except Exception as ex:
                    print(ex)
                    pass
        
        # Создаем nodes.csv
        open(f'asset/nodes_{filename}.csv', 'w', encoding='utf-8').write("id,label,weight")
        with open(f'asset/nodes_{filename}.csv', 'a', encoding='utf-8') as odin:
            #odin.write('id,label,weight')
            c = collections.Counter(names)
            users_table = []
            for i in c:
                id_stroka = i.split(',')[1]
                if id_stroka in ['id', 'label', 'weight', 'None']:
                    continue
                
                name_stroka = i.split(',')[0]
                weight = c[i]
                users_table.append([id_stroka.replace("user", ""), name_stroka, weight])
                odin.write(f'\n{id_stroka},{name_stroka},{weight}')
        
        # Вывод таблицы пользователей
        put_table(users_table, header=['USER ID', 'USERNAME', 'COUNT'])
    
    # Визуализация графа
    try:
        G = nx.DiGraph()  # Создание графа

        # Чтение узлов
        with open(f'asset/nodes_{filename}.csv', 'r', encoding='utf-8') as nodes:
            for node in nodes:
                node = node.strip()
                if node == "" or node.startswith("id,label,weight"):
                    continue  # Пропускаем заголовок и пустые строки
                
                parts = node.split(',')
                if len(parts) != 3:
                    print(f"Skipping malformed node line: {node}")
                    continue

                ids, label, weight = parts
                try:
                    weight = float(weight)  # Преобразуем в float
                    if weight < 0:
                        weight = 1
                except ValueError:
                    print(f"Invalid weight value: {weight} for node {label}. Skipping...")
                    continue

                G.add_node(label, weight=weight)
                print(f"Added node: {label} with weight: {weight}")

        # Чтение рёбер
        with open(f'asset/edges_{filename}.csv', 'r') as edges:
            for edge in edges:
                if 'source,target,label' in edge or 'None' in edge:
                    continue
                source, target, label = edge.strip().split(',')
                G.add_edge(source, target, weight=1.3)

        # Визуализация графа
        sizes = []
        colors = []
        labels = {}

        for n in G.nodes:
            weight = G.nodes[n].get('weight', 1)  # По умолчанию 1, если нет weight
            
            if isinstance(weight, (int, float)) and weight >= 0:  # Проверяем, что число неотрицательное
                min_size = 50  # Минимальный размер узла
                scale_factor = 10  # Коэффициент масштабирования

                sizes.append(max(min_size, weight * scale_factor))

                colors.append(weight)
                labels[n] = f"{n} - {weight}"  # Добавляем в labels только корректные узлы
            else:
                print(f"Invalid weight for node {n}: {weight} (type: {type(weight)})")


        pos = nx.circular_layout(G)  # Определяем расположение узлов
        nx.draw(
            G, pos, 
            with_labels=True, 
            labels=labels, 
            font_weight='bold', 
            node_size=sizes if sizes else 300,  # Значение по умолчанию
            node_color=colors if colors else "blue",  # Значение по умолчанию
            cmap=plt.cm.Blues  # Цветовая карта
        )

        plt.savefig(f'asset/{filename}.png', bbox_inches='tight')  # Сохраняем граф в файл
        plt.close()  # Закрываем график
    except Exception as ex:
        print(f"Error generating graph: {ex}")


    
    # Вывод даты первого и последнего сообщения
    firstmes = dates_list[0].replace("T", " ")
    lastmes = dates_list[-1].replace("T", " ")
    put_table([[firstmes]], header=['First Message'])
    put_table([[lastmes]], header=['Last Message'])
    
    # Отправка файлов
    try:
        nodes_content = open(f'asset/nodes_{filename}.csv', 'rb').read()
        put_file(f'nodes_{filename}.csv', label='Nodes', content=nodes_content)
    except Exception as ex:
        put_text(f"Error: {ex}")
    
    try:
        edges_content = open(f'asset/edges_{filename}.csv', 'rb').read()
        put_file(f'edges_{filename}.csv', label='Edges', content=edges_content)
    except Exception as ex:
        put_text(f"Error: {ex}")
    
    try:
        graph_content = open(f'asset/{filename}.png', 'rb').read()
        put_file(f'{filename}.png', label='Graph', content=graph_content)
    except Exception as ex:
        put_text(f"Error: {ex}")
    
    put_button("clear", onclick=lambda: run_js('window.location.reload()'))
    put_button("Scroll Up", onclick=lambda: run_js('window.scrollTo(document.body.scrollHeight, 0)'))



def start_gen():
    clear_console()
    clear()
    put_button("Scroll Down",onclick=lambda: run_js('window.scrollTo(0, document.body.scrollHeight)'))
    put_button("Return",onclick=lambda: run_js('window.location.reload()'), color='danger')
    put_html("<h1><center>Graph of Telegram Chat<center></h1><br>")
    f = file("Select a file:", accept='.json')
    open('asset/'+f['filename'], 'wb').write(f['content'])
    print(f['filename'])
    generator(f"asset/{f['filename']}")
    

def start_two():
    clear_console()
    clear()
    put_button("Scroll Down",onclick=lambda: run_js('window.scrollTo(0, document.body.scrollHeight)'))
    put_button("Return",onclick=lambda: run_js('window.location.reload()'), color='danger')
    put_html("<h1><center>Analyse of Telegram Chat<center></h1><br>")
    f = file("Select a file:", accept='.json')
    open('asset/'+f['filename'], 'wb').write(f['content'])
    filename = 'asset/'+f['filename']
    import os
    os.system(f'python words_analyze.py {filename}')
    
def start_three():
    clear_console()
    clear()
    put_button("Scroll Down",onclick=lambda: run_js('window.scrollTo(0, document.body.scrollHeight)'))
    put_html("<h1><center>Analyse of Telegram Channel<center></h1><br>")
    put_button("Return",onclick=lambda: run_js('window.location.reload()'), color='danger')
    f = file("Select a file:", accept='.json')
    open('asset/'+f['filename'], 'wb').write(f['content'])
    filename = 'asset/'+f['filename']
    import os
    channel_analyse.channel(filename)

def config():
    while True:
        clear_console()
        try:
            clear()
            put_button("Close",onclick=lambda: run_js('window.location.reload()'), color='danger')
            put_html("<h1><center>Configuration<center></h1>")
            put_text(f"select_type_stem: {read_conf('select_type_stem')}")
            put_text(f"most_common: {read_conf('most_com')}")
            put_text(f"most_common_channel: {read_conf('most_com_channel')}")
            select_type_stem = select('Stemming mode:', ['Off','On'], multiple=False)
            most_com = read_conf('most_com')
            most_com_channel = read_conf('most_com_channel')
            write_conf({"select_type_stem":select_type_stem, "most_com":most_com, "most_com_channel":most_com_channel})
            toast("Config saved.")
        except Exception as ex:
            error = f"Error: {ex}"
            toast(error)
        try:
            clear()
            put_button("Close",onclick=lambda: run_js('window.location.reload()'), color='danger')
            put_html("<h1><center>Configuration<center></h1>")
            put_text(f"select_type_stem: {read_conf('select_type_stem')}")
            put_text(f"most_common: {read_conf('most_com')}")
            put_text(f"most_common_channel: {read_conf('most_com_channel')}")
            most_com = slider('Most Common words [USER]:')
            most_com_channel = read_conf('most_com_channel')
            write_conf({"select_type_stem":select_type_stem, "most_com":most_com, "most_com_channel":most_com_channel})
            toast("Config saved.")
        except Exception as ex:
            error = f"Error: {ex}"
            toast(error)
        try:
            clear()
            put_button("Close",onclick=lambda: run_js('window.location.reload()'), color='danger')
            put_html("<h1><center>Configuration<center></h1>")
            put_text(f"select_type_stem: {read_conf('select_type_stem')}")
            put_text(f"most_common: {read_conf('most_com')}")
            put_text(f"most_common_channel: {read_conf('most_com_channel')}")
            most_com_channel = slider('Most Common words [Channel]:')
            write_conf({"select_type_stem":select_type_stem, "most_com":most_com, "most_com_channel":most_com_channel})
            toast("Config saved.")
        except Exception as ex:
            error = f"Error: {ex}"
            toast(error)

def default():
    clear()
    clear_console()
    put_button("Config", onclick=config, color='warning')
    put_html("<h1><center>Welcome to TelAnalysis<center></h1>")
    put_html("<h3>Select a module:</h3>")
    put_button("Generating Graphs", onclick=start_gen)
    put_button("Analysing Chat", onclick=start_two)
    put_button("Analysing Channel", onclick=start_three)
    
def starting():
    clear_console()
    try:
        if not os.path.exists('config.json'):
            write_conf({"select_type_stem": "Off", "most_com": 30, "most_com_channel":100})
        else:
            select_type_stem = read_conf('select_type_stem')
            most_com = read_conf('most_com')
            most_com_channel = read_conf('most_com_channel')
    except:
        write_conf({"select_type_stem": "Off", "most_com": 30, "most_com_channel":100})
        pass
    while True:
        import nltk
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('punkt_tab')

        clear_console()
        try:
            import os
            if not os.path.exists('asset'):
                os.makedirs('asset')
            open_url()
            start_server(default, host='127.0.0.1', port=9993, debug=True, background='gray')
        except KeyboardInterrupt:
            break
            exit()
        except Exception as ex:
            print(ex)
            break
    exit(1)

if __name__ == "__main__":
    starting()
