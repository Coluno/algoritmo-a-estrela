from pyamaze import maze, agent
#biblioteca para criar um estrutura de dados (fila)
from queue import  PriorityQueue

destino = (1, 1)

#função vai ser f_score = g_score(passos percorrido) + h_score(estimativa de passos)
def h_score(celula, destino):
    #definindo a possição inicial do agente
    linha_celula = celula[0]
    coluna_celula = celula[1]
    #definindo o destino
    linha_destino = destino[0]
    coluna_destino = destino[1]   
    return abs(coluna_celula - coluna_destino) + abs(linha_celula - linha_destino)

def aestrela(labirinto):
    #criar um tabuleiro
    f_score = {celula:float('inf') for celula in labirinto.grid}
    g_score = {}
    celula_inicial = (labirinto.rows, labirinto.cols)
    #calcular o valor da celula inicial
    g_score[celula_inicial] = 0
    f_score[celula_inicial] = g_score[celula_inicial] + h_score(celula_inicial,destino)

    #criando a fila
    fila = PriorityQueue()
    item_fila = (f_score[celula_inicial], h_score(celula_inicial,destino), celula_inicial)
    fila.put(item_fila)

    caminho = {} 
    while not fila.empty():
        celula = fila.get()[2]
        
        if celula == destino:
            break
        #caminhar a partir da celula inicial explorando os caminhao adjacentes
        for direcao in 'NSEW':
            if labirinto.maze_map[celula][direcao]==1:
                linha_celula = celula[0]
                colula_celula = celula[1]
                if direcao == 'N':
                    proxima_celula = (linha_celula - 1, colula_celula)
                elif direcao =='S':
                    proxima_celula = (linha_celula + 1, colula_celula)
                elif direcao == 'W':
                    proxima_celula = (linha_celula, colula_celula - 1)
                elif direcao == 'E':
                    proxima_celula = (linha_celula, colula_celula + 1)
                novo_g_score = g_score[celula] + 1
                novo_f_score = novo_g_score + h_score(proxima_celula, destino)
                #se o caminho for possivel ele deve calcular o f_score dos caminhos possiveis
                #se o f_score for menor doq a celular atual ele substitui
                #escolher o caminho com menor f_score
                if novo_f_score < f_score[proxima_celula]:
                    f_score[proxima_celula] = novo_f_score
                    g_score[proxima_celula] = novo_g_score
                    item_fila = (novo_f_score, h_score(proxima_celula, destino), proxima_celula)
                    fila.put(item_fila)
                    caminho[proxima_celula] = celula
    caminho_final = {}
    celula_analisada = destino 
    while celula_analisada != celula_inicial:
        caminho_final[caminho[celula_analisada]] = celula_analisada
        celula_analisada = caminho[celula_analisada]
    return caminho_final

#Cria um labirinto
labirinto = maze()
labirinto.CreateMaze()
#função que mostra uma lista com todas as celulas existente do labirinto print(labirinto.grid)
#Cria o agente
agente = agent(labirinto, filled=True,footprints=True)
#cria o caminho que ele vai pecorrer
caminho = aestrela(labirinto)
labirinto.tracePath({agente: caminho}, delay=100)
#print(labirinto.maze_map) função para ver o dicionario de cada celula
labirinto.run()