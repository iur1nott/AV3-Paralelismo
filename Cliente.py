import socket
import pickle
import numpy as np
import time
from matriz_utils import gerar_matriz, dividir_matriz_por_linhas, montar_matriz_de_linhas

SERVIDORES = [
    ('localhost', 5000),
    ('localhost', 5001)
]

def enviar_para_servidor(linha, matriz_b, servidor_id):
    host, port = SERVIDORES[servidor_id]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        pacote = pickle.dumps((linha, matriz_b))
        s.sendall(pacote)
        resultado = s.recv(4096)
        return pickle.loads(resultado)

def main():
    A = gerar_matriz(6, 3, aleatorio=True)
    B = gerar_matriz(3, 4, aleatorio=True)
    linhas_A = dividir_matriz_por_linhas(A)
    resultado_linhas = []

    print("[Cliente] Matriz A:\n", A)
    print("[Cliente] Matriz B:\n", B)

    inicio = time.time()
    for i, linha in enumerate(linhas_A):
        servidor_id = i % len(SERVIDORES)
        print(f"[Cliente] Enviando linha {i} para Servidor {servidor_id + 1}")
        resultado = enviar_para_servidor(linha, B, servidor_id)
        resultado_linhas.append(resultado)

    C = montar_matriz_de_linhas(resultado_linhas)
    fim = time.time()

    print("\n[Cliente] Resultado da multiplicação A x B:\n", C)
    print(f"[Cliente] Tempo total de execução: {fim - inicio:.4f} segundos")

if __name__ == '__main__':
    main()
