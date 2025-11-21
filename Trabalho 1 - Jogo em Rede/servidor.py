import socket
import os
import json

# Jogo da Velha
def desenha_tabuleiro(posicoes):
    tabuleiro = (f"| {posicoes['1']} | {posicoes['2']} | {posicoes['3']} |\n"
                 f"| {posicoes['4']} | {posicoes['5']} | {posicoes['6']} |\n"
                 f"| {posicoes['7']} | {posicoes['8']} | {posicoes['9']} |")
    print(tabuleiro)

def checa_turno(turno):
    if turno % 2 == 0: 
        return 'O' # Jogador 1 --> Servidor --> 'O'
    else:
        return 'X' # Jogador 2 --> Cliente --> 'X'

def checa_vitoria(posicoes):
    if (posicoes['1'] == posicoes['2'] == posicoes['3'] or
        posicoes['4'] == posicoes['5'] == posicoes['6'] or
        posicoes['7'] == posicoes['8'] == posicoes['9'] or
        posicoes['1'] == posicoes['4'] == posicoes['7'] or
        posicoes['2'] == posicoes['5'] == posicoes['8'] or
        posicoes['3'] == posicoes['6'] == posicoes['9'] or
        posicoes['1'] == posicoes['5'] == posicoes['9'] or
        posicoes['3'] == posicoes['5'] == posicoes['7']):
        return True
    else:
        return False


# Servidor
socket_conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
endereco = ('127.0.0.1', 50000)
socket_conexao.bind(endereco)

print("Aguardando Jogador 2 (X) se conectar...")
socket_conexao.listen(1)

sock_dados, info_cliente = socket_conexao.accept()
print(f"Jogador 2 ({info_cliente}) conectou! O jogo vai começar.")
print("Você é o Jogador 1 (O).")

# Estado do Jogo
posicoes = {str(i): str(i) for i in range(1, 10)} # Inicia dicionario
turno = 0
finalizado = False
mensagem_status = ""
codigo_status = "JOGANDO"

# Função helper para enviar o estado do jogo para o cliente
def enviar_estado(sock_cliente, board_state, status_code, message):
    try:
        estado_jogo = {
            "board": board_state,
            "status": status_code,
            "message": message
        }
        payload = json.dumps(estado_jogo).encode('utf-8')
        tamanho = len(payload).to_bytes(4, 'big')
        sock_cliente.sendall(tamanho + payload)
    except Exception as e:
        print(f"Erro ao enviar estado: {e}")
        global finalizado
        finalizado = True # Encerra o jogo se houver erro de rede

while not finalizado:
    
    jogador_atual = checa_turno(turno)
    
    #Limpa terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Jogo da Velha\n")
    desenha_tabuleiro(posicoes)

    if jogador_atual == 'O':
        enviar_estado(sock_dados, posicoes, "VEZ_OPONENTE", "Aguardando jogada do Jogador 1 (O)...")
        
        escolha = ''
        while True:
            escolha = input("\nSua vez (O). Escolha uma posição (1-9): ")
            if str.isdigit(escolha) and int(escolha) in range(1, 10) and posicoes[escolha] not in {"X", "O"}:
                break
            else:
                print("\nJogada inválida! Tente novamente.")
        
        posicoes[escolha] = 'O'

    else:
        print("\nAguardando jogada do Jogador 2 (X)...")
        enviar_estado(sock_dados, posicoes, "SUA_VEZ", "Sua vez (X):")

        try:
            # Espera a jogada --> 1 byte --> Cliente não precisa enviar nada além
            bytes_escolha = sock_dados.recv(1)
            if not bytes_escolha:
                print("Cliente desconectou.")
                finalizado = True
                continue
            
            escolha = bytes_escolha.decode('utf-8')

            if escolha == 's':
                finalizado = True
                continue

            # Valida denovo (cliente so valida posicao)
            elif str.isdigit(escolha) and int(escolha) in range(1, 10) and posicoes[escolha] not in {"X", "O"}:
                posicoes[escolha] = 'X'
                print(f"Jogador 2 (X) jogou na posição {escolha}")
            else:
                # Se o cliente enviar jogada inválida repete o turno
                print(f"Cliente enviou jogada inválida: {escolha}. Repetindo turno.")
                continue

        except Exception as e:
            print(f"Erro ao receber jogada: {e}")
            finalizado = True
            continue

    # Checar fim de jogo
    if checa_vitoria(posicoes):
        finalizado = True
        if jogador_atual == 'O':
            mensagem_status = "Jogador 1 (O) venceu!"
            codigo_status = "VITORIA_P1"
        else:
            mensagem_status = "Jogador 2 (X) venceu!"
            codigo_status = "VITORIA_P2"
    elif turno >= 8:
        finalizado = True
        mensagem_status = "Empate!"
        codigo_status = "EMPATE"
    
    # Incrementa turno (só se jogo não acabou)
    if not finalizado:
        turno += 1

# Fim do jogo
os.system('cls' if os.name == 'nt' else 'clear')

if escolha == 's':
    print("Cliente saiu da partida, encerrando jogo...\nPartida encerrada")
else:
    print("Fim de Jogo!")
    desenha_tabuleiro(posicoes)
    print(mensagem_status)

# Envia o estado final para o cliente antes de fechar conexão
enviar_estado(sock_dados, posicoes, codigo_status, mensagem_status)

sock_dados.close()
socket_conexao.close()