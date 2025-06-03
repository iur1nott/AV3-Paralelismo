import socket
import pickle
import numpy as np


HOST = 'localhost'
PORT = 5001


def multiplicar_linha(linha, matriz_b):
    return np.dot(linha, matriz_b)


# Criação e configuração do socket TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))     # Associa o socket ao IP e porta do servidor 2
    s.listen()               # Coloca o socket em modo de escuta por conexões
    print(f"[Servidor 2] Aguardando conexões em {HOST}:{PORT}...")
    # Loop principal: aceita conexões continuamente
    while True:
        conn, addr = s.accept()  # Aguarda e aceita nova conexão do cliente
        with conn:
            print(f"[Servidor 2] Conectado a {addr}")  # Log da conexão recebida

            tamanho_bytes = conn.recv(4) # recebe bytes representando tamanho
            tamanho = int.from_bytes(tamanho_bytes, 'big') # transforma em inteiro utilizável pelo Python

            if not tamanho_bytes:
                continue # Se não houver dados, ignora e espera a próxima conexão

            # recebe os dados parcialmente via bytes
            dados = b''
            while len(dados) < tamanho:
                dados += conn.recv(min(4096, tamanho - len(dados)))

            # Converte os dados de volta para objetos Python (linha e matriz)
            linha_a, matriz_b = pickle.loads(dados)

            # Realiza a multiplicação da linha por B
            resultado = multiplicar_linha(linha_a, matriz_b)

            # serializa e envia o resultado, junto com o tamanho de volta ao cliente
            resultado_bytes = pickle.dumps(resultado)
            tamanho_resultado = len(resultado_bytes)
            conn.sendall(tamanho_resultado.to_bytes(4, 'big'))
            conn.sendall(resultado_bytes)
