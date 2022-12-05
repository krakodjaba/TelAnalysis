import jmespath
import json
import collections


def one(filename):
    names = []
    open('edges.csv','w', encoding='utf-8').write("")
    open('edges.csv','a', encoding='utf-8').write("source,target,label")
    with open(filename, 'r', encoding='utf-8') as f:
        #f = f.readlines()
        jsondata = json.load(f)
        sf = jmespath.search('messages[*]',jsondata)
        for i in sf:
            fromm = jmespath.search('from', i)
            if fromm is None:
                continue
            from_id = jmespath.search('from_id',i)
            if from_id == 'source' or from_id == 'target' or from_id == 'target' or 'None' in from_id:
                continue
            else:

                name_id = f'{fromm}, {from_id}'
                names.append(name_id)  
                message = jmespath.search('text',i)
                reply_to_message_id = jmespath.search('reply_to_message_id',i)
                if reply_to_message_id is not None:
                    for i in sf:
                        message_id = jmespath.search('id', i)
                        if reply_to_message_id == message_id:
                            reply_to = jmespath.search('from', i)
                            reply_to_id = jmespath.search('from_id',i)
                            name_id = f'{reply_to}, {reply_to_id}'
                            names.append(name_id)
                            #names.append(name_id)
                            try:
                                open('edges.csv','a', encoding='utf-8').write(f'\n{from_id},{reply_to_id},{fromm}-{reply_to}')   
                            except:
                                pass
                            datas = f"""
        from: {fromm}
        from_id: {from_id}
        reply_to: {reply_to}
        reply_to_id: {reply_to_id}
        text: {message}
        """ 
                else:
                    try:
                        open('edges.csv','a', encoding='utf-8').write(f'\n{from_id},{from_id},{fromm}')  
                    except:
                        pass
                    datas = f"""
        from: {fromm}
        from_id: {from_id}
        text: {message}
        """
                print(datas)
        open('nodes.csv','w', encoding='utf-8').write("")
        with open('nodes.csv','a', encoding='utf-8') as odin:
            odin.write('id,label,weight')
            import collections
            c = collections.Counter(names)
            #stroka = name.split("',")
            for i in c:
                id_stroka = i.split(',')[1]
                if id_stroka == 'id' or id_stroka == 'label' or id_stroka == 'weight' or 'None' in id_stroka:
                    continue
                else:    
                    name_stroka = i.split(',')[0]
                    weight = c[i]
                    print(f'\n{id_stroka},{name_stroka},{weight}')
                    odin.write(f'\n{id_stroka},{name_stroka},{weight}')
    import networkx as nx
    import matplotlib.pyplot as plt
    import forceatlas2
    G=nx.DiGraph()
    with open('nodes.csv','r') as nodes:
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
                        #print(label)
                        G.add_node(label, weight=weight, node_size=weight*10, node_color=color,rescale_layout=2)
                        #print(G.nodes[1])
    
    labels = {n: f"{n} - {G.nodes[n]['weight']}" for n in G.nodes}
    colors = [G.nodes[n]['weight'] for n in G.nodes]
    sizes = [G.nodes[n]['weight']*2 for n in G.nodes]
    with open('edges.csv','r') as edges:
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
                            #print(label_from, label_to)
                            G.add_edge(label_from,label_to, weight=1.3)
                        else:
                            continue
                else:
                    continue
                
    #print(G.nodes(), G.edges())
    #G = nx.generators.ego_graph(G,1, radius=2)
    pos = nx.spring_layout(G, k=0.65, iterations=25)
    nx.draw(G,pos, with_labels=True,labels=labels,font_weight='bold', node_size=sizes, node_color=colors)
    
    #G = G.to_undirected
    #l = forceatlas2.forceatlas2_networkx_layout(G)
    plt.show()