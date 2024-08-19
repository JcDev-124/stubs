import socket
import json

def clienteStub(endereco, porta, argumentos):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((endereco, porta))

        mensagem = json.dumps(argumentos)
        s.sendall(mensagem.encode())

        mensagemResposta = s.recv(1024)

        if not mensagemResposta:
            raise ValueError("Resposta vazia recebida do servidor")

        resultado = json.loads(mensagemResposta.decode())
        return resultado

# Exemplo de uso com autenticação
argumentos = {"usuario": "user1", "senha": "password123", "op": "listar"}
resultado = clienteStub('localhost', 65000, argumentos)
print("Resultado do procedimento remoto: ", resultado)
