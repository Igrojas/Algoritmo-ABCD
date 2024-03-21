import json
import pandas as pd
import networkx as nx
from collections import defaultdict

def algoritmo_comunidad(data_autores, salida_authorrank):
    
    def create_graph(data, min_articulos_autor, min_articulos_coautor):
        """ Crea un grafo, donde se poda por número de artículos de autor principal
        y de artículos con el autor.
        Parameters:
            data: json de acuerdo a especificacion de component_def
            min_articulos: número de artículos que debe tener un autor para ingresar
            al grafo
            min_articulos_coautores: número de artículos mínimo que debe tener
            un coautor para ser considerado coautor relevante
        """
        G = nx.Graph()
        for autor_id, autor_datos in data.items():
            if autor_datos['n_articulos'] >= min_articulos_autor:
                G.add_node(autor_id)
                for  coautor_id, n in autor_datos['coautores'].items():
                    if n >= min_articulos_coautor:
                        G.add_edge(autor_id, coautor_id)
        return G

    G = create_graph(data_autores, 1, 1)
    nodos = defaultdict(lambda: 0)
    for nodo, valor in salida_authorrank[['ins', 'values']].itertuples(index=False):
        nodos[str(nodo)] = 2000 * valor

    aristas = defaultdict(lambda: 0)
    for edge in G.edges():
        aristas[edge] = data_autores[edge[0]]['coautores'][edge[1]]

    def get_peso_arista(S, key_1, key_2):
        return S.get((key_1, key_2), S.get((key_2, key_1), 0))

    def calcular_peso_promedio(el_1, el_2):
        return (len(el_1['nodos']) * el_1['peso'] + len(el_2['nodos']) * el_2['peso']) / (len(el_1['nodos']) + len(el_2['nodos']))

    def iterar_ct_S(ct, S):
        max_val = 0
        elegidos = None
        ct_keys = list(ct.keys())
        res = [peso for k, peso in S.items() if peso >= ct[k[0]]["peso"] + ct[k[1]]["peso"]]
        if res:
            max_value = max(res)
            max_keys = {key: peso for key, peso in S.items() if peso == max_value}
            for keys, peso_arista in max_keys.items():
                key_1, key_2 = keys
                peso_1 = ct[key_1]["peso"]
                peso_2 = ct[key_2]["peso"]
                if peso_arista > max_val and peso_arista >= (peso_1 + peso_2):
                    max_val = peso_arista
                    elegidos = (key_1, key_2)

        if elegidos:
            ct_new = ct.copy()
            S_new = S.copy()
            key_1, key_2 = elegidos
            new_key = f"{key_1}_{key_2}"
            el_1 = ct[key_1]
            el_2 = ct[key_2]
            peso_nuevo = calcular_peso_promedio(el_1, el_2)
            ct_new[new_key] = {"nodos": el_1['nodos'].union(el_2['nodos']), 'peso': peso_nuevo}
            del ct_new[key_1]
            del ct_new[key_2]
            # Creamos los S_new para los que corresponda
            for key_l in set(ct_keys) - {key_1, key_2}:
                q1 = len(ct[key_1]["nodos"])
                q2 = len(ct[key_2]["nodos"])
                q_dest = len(ct[key_l]["nodos"])
                s1 = get_peso_arista(S_new, key_1, key_l)
                s2 = get_peso_arista(S_new, key_2, key_l)
                s_new = (s1 * q1 * q_dest + s2 * q2 * q_dest) / ((q1 + q2) * q_dest)
                if s_new > 0:
                    S_new[(new_key, key_l)] = s_new
            for arista_n in list(S.keys()):
                if any([key_1 == x or key_2 == x for x in arista_n]):
                    del S_new[arista_n]
            return ct_new, S_new
        else:
            return ct, S

    listo = False
    ct = defaultdict(lambda: {"nodos": set(), "peso": 0})
    for x, peso in nodos.items():
        ct[x]["nodos"].add(x)
        ct[x]["peso"] = peso
    S = aristas.copy()
    iter = 1
    while not listo:
        ct_new, S_new = iterar_ct_S(ct, S)
        if len(ct_new) == 1 or len(ct_new) == len(ct):
            listo = True
        else:
            print("I", iter, ":", len(ct_new))
            ct = ct_new
            S = S_new
            iter += 1
    # print("Final 1:", S,"\n", ct)
    # print("\n")
    return ct

def sorted_cluster_by_autor(data_autores, cluster):
    # Crear el diccionario max_articulos_autor
    max_articulos_autor = {node: data['n_articulos'] for node, data in data_autores.items() if data['n_articulos'] > 0}
    max_articulos_autor = dict(sorted(max_articulos_autor.items(), key=lambda x: x[1], reverse=True))

    filter_cluster_max_autores = []
    for key in max_articulos_autor:
        for clr,data in cluster.items():
            if key in data['nodos'] and clr not in filter_cluster_max_autores:
                filter_cluster_max_autores.append(clr)

    return filter_cluster_max_autores


if __name__ == "__main__":
    f = open('data/grafo_autores.json', encoding='utf-8') 
    data_autores = json.load(f)
    f.close()

    salida_authorrank = pd.read_excel("data/salida_AuthorRank.xlsx", index_col=0)

    cluster = algoritmo_comunidad(data_autores, salida_authorrank)

    filter_cluster_max_autores = sorted_cluster_by_autor(data_autores, cluster)

    print(filter_cluster_max_autores)
