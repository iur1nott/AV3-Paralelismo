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

            dados = conn.recv(4096)  # Recebe os dados enviados (linha e matriz B)
            if not dados:
                continue  # Ignora conexões vazias ou malformadas

            # Converte os dados de volta para objetos Python (linha e matriz)
            linha_a, matriz_b = pickle.loads(dados)

            # Realiza a multiplicação da linha por B
            resultado = multiplicar_linha(linha_a, matriz_b)

            # Envia o resultado de volta ao cliente (já serializado)
            conn.sendall(pickle.dumps(resultado))
