import copy
import math
from tkinter import *


class Node:
    letra = ""
    indiceX = -1
    indiceY = -1
    fe = -1
    caminho = []
    poder = 0
    distancia_percorrida = 0
    dist_linha_reta = 0

    def __repr__(self):
        return f"No: {self.indiceX},{self.indiceY}"


labirinto = [
    ["C", "_", "_", "_", "B", "_"],
    ["_", "B", "_", "_", "_", "_"],
    ["_", "_", "F", "_", "_", "_"],
    ["_", "_", "_", "B", "B", "_"],
    ["_", "_", "_", "A", "_", "_"],
    ["_", "_", "_", "_", "_", "S"],
]


def verifica_dist_percorrida(pai, filho):
    if abs(filho.indiceX - pai.indiceX) == 1 and abs(filho.indiceY - pai.indiceY) == 1:
        return math.sqrt(2)
    else:
        return 1


def funcao_heuristica(filho, saida):
    dist_linha_reta = math.sqrt(
        (filho.indiceX - saida.indiceX) ** 2 + (filho.indiceY - saida.indiceY) ** 2
    )
    fe = filho.distancia_percorrida + dist_linha_reta
    filho.dist_linha_reta = dist_linha_reta
    return fe


def validar_movimento(labirinto, filho, poder):
    if 0 <= filho.indiceX < len(labirinto) and 0 <= filho.indiceY < len(labirinto[0]):
        letra = labirinto[filho.indiceX][filho.indiceY]
        if letra == "B" and poder == 0:
            return False
        return True
    return False


def get_menor(movimentos):
    if len(movimentos) == 0:
        return None
    menor = movimentos[1]
    indice_menor = 0
    for i in range(1, len(movimentos)):
        if movimentos[i].fe < menor.fe:
            menor = movimentos[i]
            indice_menor = i
    del movimentos[indice_menor]
    return menor


inicio = Node()
final = Node()
for i in range(len(labirinto)):
    for j in range(len(labirinto[0])):
        if labirinto[i][j] == "C":
            inicio.indiceX = i
            inicio.indiceY = j
            inicio.letra = "C"
        if labirinto[i][j] == "S":
            final.indiceX = i
            final.indiceY = j
            final.letra = "S"

possiveis_direcoes = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]
movimentos = [inicio]
visitados = []

while movimentos:
    print(f"Inicio:{inicio}")
    print(f"Final:{final}")

    if (inicio.indiceX, inicio.indiceY, inicio.poder) in visitados:
        inicio = get_menor(movimentos)
        continue
    visitados.append((inicio.indiceX, inicio.indiceY, inicio.poder))

    if inicio.indiceX == final.indiceX and inicio.indiceY == final.indiceY:
        final = inicio
        break

    for direcao in possiveis_direcoes:
        filho = Node()
        filho.indiceX = inicio.indiceX + direcao[0]
        filho.indiceY = inicio.indiceY + direcao[1]
        filho.poder = inicio.poder
        filho.caminho = inicio.caminho + [(inicio.indiceX, inicio.indiceY)]

        if validar_movimento(labirinto, filho, filho.poder):
            filho.letra = labirinto[filho.indiceX][filho.indiceY]
            if filho.letra == "F":
                filho.poder = 1
            if filho.letra == "A":
                filho.distancia_percorrida = (
                    inicio.distancia_percorrida
                    + verifica_dist_percorrida(inicio, filho)
                    + 1
                )
            else:
                filho.distancia_percorrida = (
                    inicio.distancia_percorrida
                    + verifica_dist_percorrida(inicio, filho)
                )

            filho.fe = funcao_heuristica(filho, final)
            movimentos.append(filho)
            print(
                f"Filho gerado: {filho} | FE: {filho.fe:.2f} | Dist: {filho.distancia_percorrida:.2f}"
            )

    inicio = get_menor(movimentos)
    print(f"Menor: {inicio}")
    print(f"Movimentos: {movimentos}")
    print(f"Visitados: {visitados}")
    print(f"Melhor FE: {inicio.fe}")
    print("-" * 30)

# Mostrar resultado final
if final.indiceX != -1:
    caminho_completo = final.caminho + [(final.indiceX, final.indiceY)]
    print(f"Caminho encontrado!")
    print(f"Distância total: {final.distancia_percorrida:.2f}")
    print(f"Caminho: {caminho_completo}")
else:
    print("Caminho não encontrado.")


# Classe responsável pela interface visual utilizando o tkinter
# (https://www.devmedia.com.br/tkinter-interfaces-graficas-em-python/33956)
# (https://www-codingal-com.translate.goog/coding-for-kids/blog/build-gui-games-in-python/?_x_tr_sl=en&_x_tr_tl=pt&_x_tr_hl=pt&_x_tr_pto=tc)
# (https://github.com/OtavianoSilva/minesweeper_python)


class Labirinto:
    def __init__(self, master=None):
        # Cria o frame principal para o título
        self.widget1 = Frame(master)
        self.widget1.pack()
        # Escreve o título
        self.titulo = Label(self.widget1, text="Execução do Jogo")
        self.titulo.pack()

        # Cria labirinto de acordo com a lista do labirinto definida anteriormente
        self.labirinto = Frame(master)
        self.labirinto.pack()
        cores = {
            "C": "#A8E6CF",  # Começo
            "S": "#FF8B94",  # Saída
            "A": "#AECBFA",  # Semi-barreira
            "F": "#FFFACD",  # Poder
            "B": "#6A6A6A",  # Barreira
            "_": "#FFFFFF",  # Caminho livre
        }

        for i, quadrado in enumerate(labirinto):
            for j, quadrado in enumerate(quadrado):
                cor = cores.get(quadrado, "white")  # Define a cor padrão como branco

                # Cria o label para cada quadrado do labirinto
                label = Label(
                    self.labirinto,
                    text=(
                        " " if quadrado == "_" else quadrado
                    ),  # Mostra espaço em branco para "_",
                    fg="black",  # Cor do texto
                    width=8,
                    height=4,
                    bg=cor,
                )
                # Define o espaçamento entre os labels
                label.grid(row=i, column=j, padx=2, pady=2)

        # Cria botão para sair do jogo
        self.botaoSair = Button(self.widget1, text="Sair", command=master.quit)
        self.botaoSair.pack()


root = Tk()
root.title("Atividade prática 1 - IA")  # Define o título da janela
root.geometry("800x600")  # Define o tamanho da janela
Labirinto(root)
root.mainloop()
