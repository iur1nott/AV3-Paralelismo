import numpy as np

def gerar_matriz(linhas, colunas, aleatorio=False):
    if aleatorio:
        return np.random.randint(1, 10, size=(linhas, colunas))
    else:
        return np.ones((linhas, colunas), dtype=int)

def dividir_matriz_por_linhas(matriz):
    return [linha for linha in matriz]

def montar_matriz_de_linhas(linhas):
    return np.array(linhas)
