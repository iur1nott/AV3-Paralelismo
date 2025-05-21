import multiprocessing as mp
import time

# === GRAFO MAIS COMPLEXO PARA TESTE ===
grafo = {
    'A': ['B', 'C', 'D'],
    'B': ['E', 'F'],
    'C': ['G'],
    'D': ['H', 'I'],
    'E': ['J', 'K'],
    'F': ['L'],
    'G': ['M', 'N'],
    'H': ['O'],
    'I': ['P', 'Q'],
    'J': [],
    'K': ['R'],
    'L': ['S'],
    'M': [],
    'N': ['T'],
    'O': [],
    'P': [],
    'Q': ['U', 'V'],
    'R': [],
    'S': [],
    'T': ['W'],
    'U': [],
    'V': ['X', 'Y'],
    'W': [],
    'X': [],
    'Y': ['Z'],
    'Z': []
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
    nivel = 0

    with mp.Pool(processes=num_processos) as pool:
        while nivel_atual:
            print(f"\n[Nível {nivel}] Nós a explorar: {nivel_atual}")

            # --- AGLOMERAÇÃO: dividir os nós em blocos/lotes ---
            tamanho_lote = max(1, len(nivel_atual) // num_processos)
            lotes = [nivel_atual[i:i + tamanho_lote] for i in range(0, len(nivel_atual), tamanho_lote)]

            # --- MAPEAMENTO: distribuir lotes para o pool ---
            args = [(lote, grafo, visitados) for lote in lotes]
            resultados = pool.map(processar_lote, args)

            # --- COMUNICAÇÃO: agregar os novos visitados dos subprocessos ---
            novos_nos = set().union(*resultados)
            novos_nos -= visitados  # remover duplicados já visitados
            print(f"[Nível {nivel}] Novos nós descobertos: {sorted(novos_nos)}")

            visitados.update(novos_nos)
            nivel_atual = list(novos_nos)
            nivel += 1

    return visitados

# === MEDIÇÃO DE TEMPO DE EXECUÇÃO ===
if __name__ == '__main__':
    inicio = time.time()
    resultado = bfs_paralelo_foster(grafo, 'A', num_processos=4)
    fim = time.time()

    print("\n[Resultado BFS Paralela] Nós visitados:", sorted(resultado))
    print(f"[Tempo de execução] {fim - inicio:.4f} segundos")
