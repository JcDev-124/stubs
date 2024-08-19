# README: Sistema de Autenticação com Bloqueio Automático

Este projeto é um sistema de autenticação que inclui funcionalidades para bloquear usuários após várias tentativas de login falhas e desbloquear automaticamente após um período de tempo. O sistema é implementado usando Python com sockets para comunicação cliente-servidor.

## Estrutura do Projeto

- **Servidor**: Implementa a lógica de autenticação, gerenciamento de tarefas e controle de bloqueio automático.
- **Cliente**: Conecta-se ao servidor para enviar solicitações de autenticação e operações relacionadas às tarefas.

## Funcionalidades Implementadas

1. **Autenticação de Usuário**
2. **Bloqueio de Conta após Múltiplas Tentativas Falhas**
3. **Desbloqueio Automático após um Período de Tempo**

## Passos para Implementação

### 1. **Definição de Dados e Estrutura**

- **Usuários e Senhas**: Criação de um dicionário para armazenar usuários e senhas com hashing.
- **Tentativas e Bloqueio**: Utilização de `defaultdict` para registrar tentativas de login e status de bloqueio.

### 2. **Hashing de Senha**

- **Função `hash_password`**: Implementação de uma função que utiliza SHA-256 para hash de senhas, melhorando a segurança das credenciais.

```python
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
```

### 3. **Controle de Tentativas e Bloqueio**

- **Registro de Tentativas**: Incrementa o contador de tentativas falhas para cada usuário.
- **Bloqueio**: Bloqueia o usuário após um número máximo de tentativas falhas (`MAX_TENTATIVAS`) e armazena o timestamp do bloqueio.

```python
def autenticar(usuario, senha):
    now = time.time()
    if bloqueado[usuario]["status"]:
        if now - bloqueado[usuario]["timestamp"] > TEMPO_BLOQUEIO:
            bloqueado[usuario]["status"] = False
            tentativas[usuario] = 0
        else:
            return False, "Usuário bloqueado"
    # Validação de usuário e senha...
```

### 4. **Desbloqueio Automático**

- **Desbloqueio Após Período de Tempo**: Implementação de lógica para desbloquear usuários após o tempo especificado (`TEMPO_BLOQUEIO`).

```python
if now - bloqueado[usuario]["timestamp"] > TEMPO_BLOQUEIO:
    bloqueado[usuario]["status"] = False
    tentativas[usuario] = 0
```

### 5. **Atualização do Código do Servidor**

- **Servidor Stub**: Atualização do servidor para incluir lógica de autenticação e resposta a operações baseadas na autenticação bem-sucedida ou falha.

```python
def servidorStub(porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", porta))
        s.listen()
        print("O servidor está ouvindo - porta:", porta)
        while True:
            conexaoCliente, endereco = s.accept()
            with conexaoCliente:
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
                # Processamento de operações de tarefa...
```

### 6. **Atualização do Código do Cliente**

- **Cliente Stub**: Envio de credenciais de autenticação junto com a solicitação ao servidor e processamento da resposta.

```python
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
```

## Como Executar

1. **Inicie o Servidor**:
   - Execute o script do servidor Python para iniciar o servidor e escutar na porta 65000.

   ```bash
   python servidor.py
   ```

2. **Execute o Cliente**:
   - Execute o script do cliente Python para enviar solicitações ao servidor.

   ```bash
   python cliente.py
   ```

## Dependências

- Python 3.x
- Módulos `socket`, `json`, `hashlib`, e `time` (incluídos na biblioteca padrão do Python)

## Observações

- **Segurança**: Em um ambiente de produção, considere usar autenticação mais robusta e armazenar senhas de maneira segura.
- **Manutenção**: Atualize o tempo de bloqueio e o número máximo de tentativas conforme necessário para atender aos requisitos de segurança.
