import socket
import json

tarefas = []  # "Banco de dados" simulado

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

def servidorStub(porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", porta))  # Vincula o servidor a um endereço e porta
        s.listen()  # O servidor permanecerá ouvindo
        print("O servidor está ouvindo - porta:", porta)

        while True:
            conexaoCliente, endereco = s.accept()  # Criação de objeto de comunicação com cliente

            with conexaoCliente:  # Statement usado para fechar bloco na finalização
                print("Conectado pelo cliente - IP: ", endereco)

                mensagem = conexaoCliente.recv(1024)
                if not mensagem:  # Verifica se existe algum valor em bytes dentro de mensagem
                    break  # Finaliza o bloco

                argumentos = json.loads(mensagem.decode())  # Decodificação e desserialização

                if argumentos['op'] == "adicionar":
                    resposta = addTarefa(argumentos['tarefa'])
                elif argumentos['op'] == 'remover':
                    resposta = removeTarefa(argumentos['id'])
                elif argumentos['op'] == 'listar':
                    resposta = listTarefa()
                else:
                    resposta = "Operação inválida"

                reply = json.dumps(resposta)  # Processo de serialização
                conexaoCliente.sendall(reply.encode())  # Envio do retorno e a codificação

servidorStub(65000)
