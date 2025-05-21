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

# === BFS SEQUENCIAL ===
def bfs_sequencial(grafo, inicio):
    visitados = set([inicio])
    nivel_atual = [inicio]
    nivel = 0

    while nivel_atual:
        print(f"\n[Nível {nivel}] Nós a explorar: {nivel_atual}")
        novos_nos = []

        for no in nivel_atual:
            for vizinho in grafo.get(no, []):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    novos_nos.append(vizinho)

        print(f"[Nível {nivel}] Novos nós descobertos: {sorted(novos_nos)}")
        nivel_atual = novos_nos
        nivel += 1

    return visitados

# === MEDIÇÃO DE TEMPO DE EXECUÇÃO ===
if __name__ == '__main__':
    inicio = time.time()
    resultado = bfs_sequencial(grafo, 'A')
    fim = time.time()

    print("\n[Resultado BFS Sequencial] Nós visitados:", sorted(resultado))
    print(f"[Tempo de execução] {fim - inicio:.4f} segundos")
