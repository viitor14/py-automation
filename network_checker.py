# network_checker.py
import socket

def check_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Tenta criar uma conexão de socket com um host externo para verificar a conectividade.
    8.8.8.8 (servidor DNS do Google) na porta 53 (DNS) é um alvo confiável e rápido.
    Retorna True se a conexão for bem-sucedida, False caso contrário.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(f"Sem conexão com a internet: {ex}")
        return False