import socket
import os
import json

# Jogo da Velha
def desenha_tabuleiro(posicoes):
    tabuleiro = (f"| {posicoes['1']} | {posicoes['2']} | {posicoes['3']} |\n"
                 f"| {posicoes['4']} | {posicoes['5']} | {posicoes['6']} |\n"
                 f"| {posicoes['7']} | {posicoes['8']} | {posicoes['9']} |")
    print(tabuleiro)

# Cliente
sock_dados = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
endereco_servidor = ('127.0.0.1', 50000)

try:
    sock_dados.connect(endereco_servidor)
    print("Conectado ao servidor! Você é o Jogador 2 (X).")
except Exception as e:
    print(f"Não foi possível conectar ao servidor: {e}")
    exit()

jogo_ativo = True
while jogo_ativo:
    try:
        # Recebe cabeçalho com tamanho do payload
        tam_bytes = sock_dados.recv(4)
        if not tam_bytes:
            print("Servidor desconectou (cabeçalho).")
            jogo_ativo = False
            continue
        
        tam_int = int.from_bytes(tam_bytes, 'big')

        # Recebe payload
        payload_bytes = sock_dados.recv(tam_int)
        if not payload_bytes:
            print("Servidor desconectou (payload).")
            jogo_ativo = False
            continue

        # Transforma JSON pra dicionario
        estado_jogo = json.loads(payload_bytes.decode('utf-8'))

        posicoes = estado_jogo['board']
        status = estado_jogo['status']
        message = estado_jogo['message']

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Jogo da Velha - Envie 's' para sair\n")
        desenha_tabuleiro(posicoes)
        print(f"\n{message}")

        # Checa status do jogo
        if status == "SUA_VEZ":
            escolha = ''
            while True:
                escolha = input()
                if escolha == 's':
                    break
                elif str.isdigit(escolha) and int(escolha) in range(1, 10):
                    # Checagem rápida, servidor checa full
                    if posicoes[escolha] not in {"X", "O"}:
                        break
                    else:
                        print("Posição já ocupada! Tente novamente.")
                else:
                    print("Jogada inválida! Tente novamente.")
            
            # Envia apenas o byte da jogada (ou s para fechar conexão)
            if escolha == 's': 
                sock_dados.send(escolha.encode('utf-8'))
                print("Saindo do jogo...")
                jogo_ativo = False
            else:
                sock_dados.send(escolha.encode('utf-8'))


        elif status == "VEZ_OPONENTE":
            print("")
            # Loop continua
        
        elif status in ["VITORIA_P1", "VITORIA_P2", "EMPATE"]:
            os.system('cls' if os.name == 'nt' else 'clear')
            desenha_tabuleiro(posicoes)
            print("Fim de jogo.")
            print(message)
            jogo_ativo = False # Encerra o loop

    except Exception as e:
        print(f"Erro de comunicação: {e}")
        jogo_ativo = False

print("Conexão encerrada.")
sock_dados.close()