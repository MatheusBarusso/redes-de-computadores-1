# Implementação de uma Aplicação de Rede

## Sobre a atividade

O objetivo desta atividade é compreender o processo de desenvolvimento de uma aplicação de rede utilizando sockets, considerando os tipos e a ordem das mensagens, além do comportamento de clientes e servidores. Vocês deverão implementar um jogo com pelo menos dois jogadores, utilizando sockets TCP, escolhidos pelas garantias de confiabilidade e ordenação dos segmentos. Os testes devem ser realizados utilizando localhost (127.0.0.1) devido às dificuldades relacionadas à tradução de endereços para usuários domésticos.

## Requisitos da Implementação

A implementação será avaliada com base nos seguintes critérios:

- Seguir as regras do jogo escolhido
- Implementação correta no contexto de redes
- Cumprir todos os requisitos mínimos descritos

### Jogos permitidos

Qualquer jogo por turnos, ou seja, que envolva mais de uma interação entre cliente e servidor, está permitido. Exemplos adequados:

- Jogo da velha

- Forca

- Jogos de cartas que seguem turnos

### Não é permitido implementar jogos cuja dinâmica de turnos só existe porque a partida é repetida, como:

- Jo-ken-po (pedra-papel-tesoura)

- Par ou ímpar

- Dois ou um

- Jogos semelhantes aos anteriores

## Interface

Não é necessária interface gráfica elaborada. Basta exibir as informações mínimas para que o jogador possa realizar suas ações, podendo utilizar uma interface simplificada (ex.: terminal).