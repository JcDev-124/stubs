import socket
import json
from collections import defaultdict
import hashlib
import time

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# "Banco de dados" simulado
tarefas = []
usuarios = {
    "user1": hash_password("password123")}  # Usuários e senhas (em um sistema real, use hashing e armazenamento seguro)
tentativas = defaultdict(int)  # Registro das tentativas de login
bloqueado = defaultdict(lambda: {"status": False, "timestamp": 0})  # Status de bloqueio e timestamp
MAX_TENTATIVAS = 3  # Máximo de tentativas antes do bloqueio
TEMPO_BLOQUEIO = 60  # Tempo em segundos para desbloqueio automático



def addTarefa(tarefa):
    tarefaDesc = {"id": len(tarefas) + 1, "tarefa": tarefa}
    tarefas.append(tarefaDesc)
    return f"Tarefa: '{tarefa}' adicionada com sucesso"


def removeTarefa(idTarefa):
    for tarefa in tarefas:
        if tarefa["id"] == idTarefa:
            tarefas.remove(tarefa)
            return f"Tarefa: '{tarefa['tarefa']}' removida com sucesso"
    return "ID não identificado"


def listTarefa():
    if not tarefas:
        return "Nenhuma tarefa encontrada"
    return tarefas


def autenticar(usuario, senha):
    now = time.time()
    if bloqueado[usuario]["status"]:
        if now - bloqueado[usuario]["timestamp"] > TEMPO_BLOQUEIO:
            # Desbloqueia o usuário após o tempo de bloqueio
            bloqueado[usuario]["status"] = False
            tentativas[usuario] = 0
        else:
            return False, "Usuário bloqueado"

    if usuario in usuarios and hash_password(senha) == usuarios[usuario]:
        tentativas[usuario] = 0  # Resetar tentativas após login bem-sucedido
        return True, "Autenticação bem-sucedida"

    tentativas[usuario] += 1
    if tentativas[usuario] >= MAX_TENTATIVAS:
        bloqueado[usuario]["status"] = True
        bloqueado[usuario]["timestamp"] = now
        return False, "Usuário bloqueado após muitas tentativas"

    return False, "Usuário ou senha incorretos"


def servidorStub(porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", porta))
        s.listen()
        print("O servidor está ouvindo - porta:", porta)

        while True:
            conexaoCliente, endereco = s.accept()

            with conexaoCliente:
                print("Conectado pelo cliente - IP: ", endereco)

                mensagem = conexaoCliente.recv(1024)
                if not mensagem:
                    break

                dados = json.loads(mensagem.decode())

                usuario = dados.get("usuario")
                senha = dados.get("senha")
                if usuario and senha:
                    autenticado, resposta = autenticar(usuario, senha)
                    if not autenticado:
                        reply = json.dumps(resposta)
                        conexaoCliente.sendall(reply.encode())
                        continue

                op = dados.get("op")
                if op == "adicionar":
                    resposta = addTarefa(dados.get('tarefa'))
                elif op == 'remover':
                    resposta = removeTarefa(dados.get('id'))
                elif op == 'listar':
                    resposta = listTarefa()
                else:
                    resposta = "Operação inválida"

                reply = json.dumps(resposta)
                conexaoCliente.sendall(reply.encode())


servidorStub(65000)
