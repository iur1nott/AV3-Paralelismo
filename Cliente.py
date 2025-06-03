import socket
import pickle
import numpy as np
import time
from matriz_utils import gerar_matriz, dividir_matriz_por_linhas, montar_matriz_de_linhas


SERVIDORES = [
    ('localhost', 5000),  # Servidor 1 (porta 5000)
    ('localhost', 5001)   # Servidor 2 (porta 5001)
]



def enviar_para_servidor(linha, matriz_b, servidor_id):
    host, port = SERVIDORES[servidor_id]  # Seleciona o servidor de destino
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))  # Estabelece conexão com o servidor
        pacote = pickle.dumps((linha, matriz_b))  # Serializa a linha de A e matriz B

        # Lógica para enviar dados de tamanho dinâmico
        tamanho_pacote = len(pacote)
        s.sendall(tamanho_pacote.to_bytes(4, 'big')) # enviando bytes representando o tamanho do pacote
        s.sendall(pacote)

        # recebe o resultado parcialmente até completar os dados
        tamanho_resultado = int.from_bytes(s.recv(4), 'big')

        # em Python b'' representa um byte literal vazio, 
        # pra ser preenchido com dados recebidos via socket
        resultado_bytes = b''
        while len(resultado_bytes) < tamanho_resultado:
            # uso 4096 bytes como base de forma arbitrária, talvez um tamanho
            # muito pequeno cause overhead de tráfego TCP/IP
            resultado_bytes += s.recv(min(4096, tamanho_resultado - len(resultado_bytes)))
        
        # retorna os bytes desserializados
        return pickle.loads(resultado_bytes)


def main():
    # Gera matrizes com valores aleatórios: A (6x3), B (3x4)
    A = gerar_matriz(256, 4096, aleatorio=True)
    B = gerar_matriz(4096, 64, aleatorio=True)

    # Divide a matriz A em linhas individuais para distribuir aos servidores
    linhas_A = dividir_matriz_por_linhas(A)
    resultado_linhas = []  # Lista que armazenará as linhas multiplicadas (resultado)

    # Exibe as matrizes originais no terminal
    print("[Cliente] Matriz A:\n", A)
    print("[Cliente] Matriz B:\n", B)

    # Marca o tempo de início da execução
    inicio = time.time()

    # Envia cada linha de A para um servidor de forma alternada (round-robin)
    for i, linha in enumerate(linhas_A):
        servidor_id = i % len(SERVIDORES)  # Alterna entre os servidores disponíveis
        print(f"[Cliente] Enviando linha {i} para Servidor {servidor_id + 1}")
        resultado = enviar_para_servidor(linha, B, servidor_id)  # Envia e recebe o resultado
        resultado_linhas.append(resultado)  # Armazena a linha resultante

    # Reconstrói a matriz final a partir das linhas retornadas pelos servidores
    C = montar_matriz_de_linhas(resultado_linhas)

    # Marca o tempo de término da execução
    fim = time.time()

    # Exibe o resultado final e o tempo de execução
    print("\n[Cliente] Resultado da multiplicação A x B:\n", C)
    print(f"[Cliente] Tempo total de execução: {fim - inicio:.4f} segundos")
    inicio = time.time()
    np.dot(A,B)
    fim = time.time()
    print(f"[Cliente] Tempo de execução serial: {fim - inicio:.4f} segundos")

# Ponto de entrada do programa
if __name__ == '__main__':
    main()
