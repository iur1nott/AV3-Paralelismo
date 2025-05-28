import socket
import pickle
import numpy as np

HOST = 'localhost'
PORT = 5000

def multiplicar_linha(linha, matriz_b):
    return np.dot(linha, matriz_b)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[Servidor 1] Aguardando conexões em {HOST}:{PORT}...")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"[Servidor 1] Conectado a {addr}")
            dados = conn.recv(4096)
            if not dados:
                continue
            linha_a, matriz_b = pickle.loads(dados)
            resultado = multiplicar_linha(linha_a, matriz_b)
            conn.sendall(pickle.dumps(resultado))
