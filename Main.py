import socket
import pickle
import numpy as np
from matriz_utils import gerar_matriz, dividir_matriz_por_linhas, montar_matriz_de_linhas

HOST = 'localhost'
PORT = 5000

def main():
    print("[Cliente] Gerando matrizes A e B...")
    A = gerar_matriz(4, 3, aleatorio=True)
    B = gerar_matriz(3, 2, aleatorio=True)

    print("[Cliente] Matriz A:\n", A)
    print("[Cliente] Matriz B:\n", B)

    linhas_A = dividir_matriz_por_linhas(A)
    resultado_linhas = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        for linha in linhas_A:
            pacote = pickle.dumps((linha, B))
            s.sendall(pacote)

            dados_recebidos = s.recv(4096)
            linha_resultado = pickle.loads(dados_recebidos)
            resultado_linhas.append(linha_resultado)

    C = montar_matriz_de_linhas(resultado_linhas)
    print("[Cliente] Resultado da multiplicação A x B:\n", C)

if __name__ == '__main__':
    main()
