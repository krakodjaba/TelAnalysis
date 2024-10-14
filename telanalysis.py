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


global select_type_stem


## config pywebio
config(theme='dark',title="TelAnalysis", description="Analysing Telegram CHATS-CHANNELS-GROUPS")


def generator(filename):
    tables = []
    clear_console()
    filename = filename.split(".")[0]
    filename = filename.split("/")[1]
    dates_list = list()
    names = []
    open(f'asset/edges_{filename}.csv','w', encoding='utf-8').write("")
    open(f'asset/edges_{filename}.csv','a', encoding='utf-8').write("source,target,label")
    with open(f'asset/{filename}.json', 'r', encoding='utf-8') as f:
        jsondata = json.load(f)
        group_name = jmespath.search('name', jsondata)
        put_html(f"<center><h1>{group_name}</h1><center>")
        sf = jmespath.search('messages[*]',jsondata)
        toast(content='Wait Result..',duration=0)
        for i in sf:
            fromm = jmespath.search('from', i)
            if fromm is None:
                continue
            from_id = jmespath.search('from_id',i)
            date = jmespath.search('date', i)
            dates_list.append(date)
            if from_id == 'source' or from_id == 'target' or from_id == 'target' or 'None' in from_id:
                continue
            else:

                name_id = f'{fromm}, {from_id}'
                names.append(name_id)  
                message = jmespath.search('text',i)
                if str(type(message)) == "<class 'list'>":
                    for textt in message:
                        try:
                            test = textt['text']
                            test = test.replace("\\n","").replace("\n","").strip()
                            try:
                                message = remove_emojis(test)
                            except:
                                message = test
                        except Exception as ex:
                            error = f"Error: {ex}"
                            continue
                else:
                    try:
                        message = remove_emojis(message)
                    except:
                        message = message
                if message == "":
                    continue
                else:
                    reply_to_message_id = jmespath.search('reply_to_message_id',i)
                    if reply_to_message_id is not None:
                        for i in sf:
                            message_id = jmespath.search('id', i)
                            if reply_to_message_id == message_id:
                                reply_to = jmespath.search('from', i)
                                reply_to_id = jmespath.search('from_id',i)
                                name_id = f'{reply_to}, {reply_to_id}'
                                names.append(name_id)
                                try:
                                    open(f'asset/edges_{filename}.csv','a', encoding='utf-8').write(f'\n{from_id},{reply_to_id},{fromm}-{reply_to}')   
                                except Exception as ex:
                                    print(ex)
                                    pass
                               
                    else:
                        try:
                            open(f'asset/edges_{filename}.csv','a', encoding='utf-8').write(f'\n{from_id},{from_id},{fromm}')  
                        except Exception as ex:
                            print(ex)
                            pass
        open(f'asset/nodes_{filename}.csv','w', encoding='utf-8').write("")
        with open(f'asset/nodes_{filename}.csv','a', encoding='utf-8') as odin:
            odin.write('id,label,weight')
            c = collections.Counter(names)
            users_table = []
            for i in c:
                id_stroka = i.split(',')[1]
                if id_stroka == 'id' or id_stroka == 'label' or id_stroka == 'weight' or 'None' in id_stroka:
                    continue
                else:    
                    name_stroka = i.split(',')[0]
                    weight = c[i]
                    users_table.append([id_stroka.replace("user",""), name_stroka, weight])
                    odin.write(f'\n{id_stroka},{name_stroka},{weight}')
        
    put_table(users_table, header=['USER ID','USERNAME','COUNT'])
    
    try:
        G=nx.DiGraph()
        with open(f'asset/nodes_{filename}.csv','r') as nodes:
            for node in nodes:
                if 'source,target,label' in node or 'None' in node:
                    continue
                else:
                    node = node.replace("\n","")
                    nn_nodes = []
                    node = node.split(",")
                    ids = node[0]
                    label = node[1]
                    if 'source' in label or 'target' in label or 'label' in label:
                        continue

                    else:
                        weight = node[2]
                        weight = int(weight)
                        if weight <=10:
                            color = 'yellow'
                        elif weight >= 10 and weight <= 100:
                            color = 'green'
                        elif weight >= 100 and weight <= 500:
                            color = 'blue'
                        elif weight >= 500:
                            color = 'red'
                        if label not in nn_nodes:
                            nn_nodes.append(label)
                            G.add_node(label, weight=weight, node_size=weight*8, node_color=color,rescale_layout=2)
        
        labels = {n: f"{n} - {G.nodes[n]['weight']}" for n in G.nodes}
        colors = [G.nodes[n]['weight'] for n in G.nodes]
        sizes = [G.nodes[n]['weight']*2 for n in G.nodes]
        with open(f'asset/edges_{filename}.csv','r') as edges:
            nn_edges = []
            for edge in edges:
                if 'source,target,label' in edge or 'None' in edge:
                    continue
                else:
                    if edge not in nn_edges:
                        nn_edges.append(edge)
                        edge = edge.split(",")
                        source = edge[0]
                        target = edge[1]
                        try:
                            label_from = str(edge[2]).split("-")[0]
                            label_from = str(label_from).replace("\n","")
                        except:
                            label_from = ''
                        try:
                            label_to = str(edge[2]).split("-")[1]
                            label_to = str(label_to).replace("\n","")
                        except:
                            label_to = ''
                        if label_from == label_to or label_from == '' or label_to == '':
                            continue
                        else:
                            if f'{label_from} {label_to}' not in nn_edges:
                                nn_edges.append(f'{label_from} {label_to}')
                                G.add_edge(label_from,label_to, weight=1.3)
                            else:
                                continue
                    else:
                        continue
    except Exception as ex:
        print(ex)
        pass

    firstmes = str(dates_list[:1]).replace("[","").replace("]","").replace("'","").replace("T"," ")
    lastmes = str(dates_list[-1:]).replace("[","").replace("]","").replace("'","").replace("T"," ")
    firstmess = []
    lastmess = []
    lastmess.append(lastmes)
    firstmess.append(firstmes)
    put_table([firstmess], header=['First Message'])
    put_table([lastmess], header=['Last Message'])
    
    try:
        try:
            pos = nx.circular_layout(G)
        except:
            put_text("error #14")
        try:

            nx.draw(G,pos, with_labels=True,labels=labels,font_weight='bold', node_size=sizes, node_color=colors)
            try:
                plt.savefig(f'asset/{filename}.png', bbox_inches='tight')
                img = open(f'asset/{filename}.png','rb').read()
            except Exception as ex:
                print(ex)
                es = " error #16"
                put_text(es)
            try:
                put_image(img, width='600px')
            except Exception as ex:
                put_text(f"Error: {ex}")
        except Exception as ex:
            put_html(f"error #15 {ex}<br>Perhaps the chat is too large, the preliminary graph could not be generated.<br>Try to make graph in Gephi with below files.")
    except Exception as ex:
        put_text(f"Error in generating image.:{ex}")
    put_text("Files:")
    try:
        nodes_content = open(f'asset/nodes_{filename}.csv', 'rb').read()
        put_file(f'asset/nodes_{filename}.csv',label='Nodes',content=nodes_content)
    except Exception as ex:
        put_text(f"error: {ex}")
    try:
        edges_content = open(f'asset/edges_{filename}.csv', 'rb').read()
        put_file(f'asset/edges_{filename}.csv',label='Edges', content=edges_content)
    except Exception as ex:
        put_text(f"error: {ex}")
    try:
        Graph_content = open(f'asset/{filename}.png', 'rb').read()
        put_file(f'asset/{filename}.png',label='Graph', content=Graph_content)
    except Exception as ex:
        pass
    put_button("clear",onclick=lambda: run_js('window.location.reload()'))
    put_button("Scroll Up",onclick=lambda: run_js('window.scrollTo(document.body.scrollHeight, 0)'))


def start_gen():
    clear_console()
    clear()
    put_button("Scroll Down",onclick=lambda: run_js('window.scrollTo(0, document.body.scrollHeight)'))
    put_button("Return",onclick=lambda: run_js('window.location.reload()'), color='danger')
    put_html("<h1><center>Graph of Telegram Chat<center></h1><br>")
    f = file("Select a file:", accept='.json')
    open('asset/'+f['filename'], 'wb').write(f['content'])
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
    os.system(f'python3 words_analyze.py {filename}')
    
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
