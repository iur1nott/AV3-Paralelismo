import multiprocessing as mp

# === GRAFO DE TESTE ===
grafo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [],
    'E': ['H'],
    'F': [],
    'G': ['H'],
    'H': []
}

# === FUNÇÃO DE PROCESSAMENTO DE UM LOTE DE NÓS ===
def processar_lote(args):
    lote_nos, grafo, visitados = args
    novos = set()
    for no in lote_nos:
        for vizinho in grafo.get(no, []):
            if vizinho not in visitados:
                novos.add(vizinho)
    return novos

# === BFS PARALELA USANDO POOL COM METODOLOGIA DE FOSTER ===
def bfs_paralelo_foster(grafo, inicio, num_processos=4):
    visitados = set([inicio])
    nivel_atual = [inicio]

    with mp.Pool(processes=num_processos) as pool:
        while nivel_atual:
            # --- AGLOMERAÇÃO: dividir os nós em blocos/lotes ---
            tamanho_lote = max(1, len(nivel_atual) // num_processos)
            lotes = [nivel_atual[i:i + tamanho_lote] for i in range(0, len(nivel_atual), tamanho_lote)]

            # --- MAPEAMENTO: distribuir lotes para o pool ---
            args = [(lote, grafo, visitados) for lote in lotes]
            resultados = pool.map(processar_lote, args)

            # --- COMUNICAÇÃO: agregar os novos visitados dos subprocessos ---
            novos_nos = set().union(*resultados)
            novos_nos -= visitados  # remover duplicados já visitados
            visitados.update(novos_nos)
            nivel_atual = list(novos_nos)

    return visitados

if __name__ == '__main__':
    resultado = bfs_paralelo_foster(grafo, 'A', num_processos=4)
    print("[Resultado BFS Paralela] Nós visitados:", resultado)
