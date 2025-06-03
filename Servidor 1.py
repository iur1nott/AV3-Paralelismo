import socket
import pickle
import numpy as np

HOST = 'localhost'
PORT = 5000



def multiplicar_linha(linha, matriz_b):
    return np.dot(linha, matriz_b)

# Criação de um socket TCP e associação a um endereço específico
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))     # Associa o socket ao IP e porta definidos para o servidor
    s.listen()               # Coloca o servidor em estado de escuta, aguardando conexões
    print(f"[Servidor 1] Aguardando conexões em {HOST}:{PORT}...")

    # Laço infinito para aceitar múltiplas conexões de clientes (cada uma por linha recebida)
    while True:
        conn, addr = s.accept()  # Aceita uma nova conexão
        with conn:
            print(f"[Servidor 1] Conectado a {addr}")  # Mostra o endereço do cliente conectado
            
            tamanho_bytes = conn.recv(4) # recebe bytes representando tamanho
            tamanho = int.from_bytes(tamanho_bytes, 'big') # transforma em inteiro utilizável pelo Python

            if not tamanho_bytes:
                continue # Se não houver dados, ignora e espera a próxima conexão

            # recebe os dados parcialmente via bytes
            dados = b''
            while len(dados) < tamanho:
                dados += conn.recv(min(4096, tamanho - len(dados)))

            # Desserializa os dados recebidos: uma linha da matriz A e a matriz B
            linha_a, matriz_b = pickle.loads(dados)

            # Realiza a multiplicação da linha por B
            resultado = multiplicar_linha(linha_a, matriz_b)

            # serializa e envia o resultado, junto com o tamanho de volta ao cliente
            resultado_bytes = pickle.dumps(resultado)
            tamanho_resultado = len(resultado_bytes)
            conn.sendall(tamanho_resultado.to_bytes(4, 'big'))
            conn.sendall(resultado_bytes)