import json
import jmespath
import collections
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

GRAPH_DIR = "graphs"
os.makedirs(GRAPH_DIR, exist_ok=True)

def generate_graph_from_file(filepath: str) -> dict:
    filename = os.path.basename(filepath).split(".")[0]

    edges_path = os.path.join(GRAPH_DIR, f'edges_{filename}.csv')
    nodes_path = os.path.join(GRAPH_DIR, f'nodes_{filename}.csv')
    png_path = os.path.join(GRAPH_DIR, f'{filename}.png')
    json_path = os.path.join(GRAPH_DIR, f'{filename}.json')  # D3 graph json

    # Загружаем JSON с сообщениями
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    messages = jmespath.search('messages[*]', data) or []

    names = []
    edges = []

    # Генерация edges
    for msg in messages:
        fromm = msg.get('from')
        from_id = msg.get('from_id')
        if not fromm or not from_id:
            continue
        names.append(f"{fromm},{from_id}")

        reply_id = msg.get('reply_to_message_id')
        if reply_id:
            reply_msg = next((m for m in messages if m.get('id') == reply_id), None)
            if reply_msg:
                reply_to = reply_msg.get('from')
                reply_to_id = reply_msg.get('from_id')
                if reply_to and reply_to_id:
                    names.append(f"{reply_to},{reply_to_id}")
                    edges.append({
                        "source": from_id,
                        "target": reply_to_id,
                        "label": f"{fromm}-{reply_to}"
                    })
        else:
            # Петля для одиночного сообщения
            edges.append({
                "source": from_id,
                "target": from_id,
                "label": fromm
            })

    # Создание узлов с весами
    counter = collections.Counter(names)
    nodes = []
    for i in counter:
        id_str = i.split(',')[1]
        name_str = i.split(',')[0]
        if not id_str or id_str == 'None':
            continue
        nodes.append({
            "id": id_str,
            "label": name_str,
            "weight": counter[i]
        })

    # Отфильтровываем edges, чтобы все ссылки были на существующие nodes
    node_ids = {n['id'] for n in nodes}
    edges = [e for e in edges if e['source'] in node_ids and e['target'] in node_ids]

    # Запись CSV
    with open(edges_path, 'w', encoding='utf-8') as efile:
        efile.write("source,target,label\n")
        for e in edges:
            efile.write(f"{e['source']},{e['target']},{e['label']}\n")

    with open(nodes_path, 'w', encoding='utf-8') as nfile:
        nfile.write("id,label,weight\n")
        for n in nodes:
            nfile.write(f"{n['id']},{n['label']},{n['weight']}\n")

    # Генерация D3 JSON
    graph_json = {"nodes": nodes, "links": edges}
    with open(json_path, 'w', encoding='utf-8') as jf:
        json.dump(graph_json, jf, ensure_ascii=False, indent=2)


    return {
        "json": f"/graphs/{filename}.json"
    }
