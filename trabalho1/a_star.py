import math
from copy import deepcopy

class Node:
    def __init__(self):
        self.letra = ""
        self.indiceX = -1
        self.indiceY = -1
        self.fe = -1
        self.caminho = []
        self.poder = 0
        self.distancia_percorrida = 0
        self.dist_linha_reta = 0

    def __repr__(self):
        return f"No: {self.indiceX},{self.indiceY}"

def verifica_dist_percorrida(pai, filho):
    if abs(filho.indiceX - pai.indiceX) == 1 and abs(filho.indiceY - pai.indiceY) == 1:
        return math.sqrt(2)
    else:
        return 1

def funcao_heuristica(filho, saida):
    dist_linha_reta = math.sqrt((filho.indiceX - saida.indiceX)**2 + (filho.indiceY - saida.indiceY)**2)
    fe = filho.distancia_percorrida + dist_linha_reta
    filho.dist_linha_reta = dist_linha_reta
    return fe

def validar_movimento(labirinto, filho, poder):
    if 0 <= filho.indiceX < len(labirinto) and 0 <= filho.indiceY < len(labirinto[0]):
        letra = labirinto[filho.indiceX][filho.indiceY]
        if letra == 'B' and poder == 0:
            return False
        return True
    return False

def get_menor(movimentos):
    if not movimentos:
        return None
    menor = movimentos[0]
    indice_menor = 0
    for i in range(1, len(movimentos)):
        if movimentos[i].fe < menor.fe:
            menor = movimentos[i]
            indice_menor = i
    del movimentos[indice_menor]
    return menor

def executar_busca(labirinto):
    inicio = Node()
    final = Node()

    for i in range(len(labirinto)):
        for j in range(len(labirinto[0])):
            if labirinto[i][j] == 'C':
                inicio.indiceX = i
                inicio.indiceY = j
                inicio.letra = 'C'
            if labirinto[i][j] == 'S':
                final.indiceX = i
                final.indiceY = j
                final.letra = 'S'

    possiveis_direcoes = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    movimentos = [inicio]
    visitados = []
    historico_passos = []

    while movimentos:
        if (inicio.indiceX, inicio.indiceY, inicio.poder) in visitados:
            inicio = get_menor(movimentos)
            continue
        visitados.append((inicio.indiceX, inicio.indiceY, inicio.poder))

        estado_atual = {
            'pos': (inicio.indiceX, inicio.indiceY),
            'filhos': [],
            'fe': inicio.fe,
        }

        if inicio.indiceX == final.indiceX and inicio.indiceY == final.indiceY:
            final = inicio
            historico_passos.append(estado_atual)
            break

        for direcao in possiveis_direcoes:
            filho = Node()
            filho.indiceX = inicio.indiceX + direcao[0]
            filho.indiceY = inicio.indiceY + direcao[1]
            filho.poder = inicio.poder
            filho.caminho = inicio.caminho + [(inicio.indiceX, inicio.indiceY)]

            if validar_movimento(labirinto, filho, filho.poder):
                filho.letra = labirinto[filho.indiceX][filho.indiceY]
                if filho.letra == 'F':
                    filho.poder = 1
                if filho.letra == 'A':
                    filho.distancia_percorrida = inicio.distancia_percorrida + verifica_dist_percorrida(inicio, filho) + 1
                else:
                    filho.distancia_percorrida = inicio.distancia_percorrida + verifica_dist_percorrida(inicio, filho)

                filho.fe = funcao_heuristica(filho, final)
                movimentos.append(filho)
                estado_atual['filhos'].append((filho.indiceX, filho.indiceY, filho.fe))

        historico_passos.append(estado_atual)
        inicio = get_menor(movimentos)

    if final.indiceX != -1:
        caminho_completo = final.caminho + [(final.indiceX, final.indiceY)]
        return caminho_completo, final.distancia_percorrida, historico_passos
    else:
        return None, None, historico_passos
