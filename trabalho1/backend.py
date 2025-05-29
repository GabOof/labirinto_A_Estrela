import math
from tkinter import *


class Node:
    def __init__(self, x=-1, y=-1, letra="", poder=0):
        self.indiceX = x
        self.indiceY = y
        self.letra = letra
        self.poder = poder
        self.fe = -1
        self.caminho = []
        self.distancia_percorrida = 0
        self.dist_linha_reta = 0

    def __repr__(self):
        return f"No({self.indiceX},{self.indiceY}) FE={self.fe:.2f} Poder={self.poder}"


# Labirinto inicial
labirinto = [
    ["C", "_", "_", "_", "B", "_"],
    ["_", "B", "_", "_", "_", "_"],
    ["_", "_", "F", "_", "_", "_"],
    ["_", "_", "_", "B", "B", "_"],
    ["_", "_", "_", "A", "_", "_"],
    ["_", "_", "_", "_", "_", "S"],
]

direcoes = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]


def verifica_dist_percorrida(pai, filho):
    # Diagonal = sqrt(2), reta = 1
    if abs(filho.indiceX - pai.indiceX) == 1 and abs(filho.indiceY - pai.indiceY) == 1:
        return math.sqrt(2)
    return 1


def funcao_heuristica(filho, saida):
    dist_linha_reta = math.sqrt(
        (filho.indiceX - saida.indiceX) ** 2 + (filho.indiceY - saida.indiceY) ** 2
    )
    filho.dist_linha_reta = dist_linha_reta
    return filho.distancia_percorrida + dist_linha_reta


def validar_movimento(lab, nodo, poder):
    x, y = nodo.indiceX, nodo.indiceY
    if 0 <= x < len(lab) and 0 <= y < len(lab[0]):
        letra = lab[x][y]
        if letra == "B" and poder == 0:
            return False
        return True
    return False


def get_menor(movs):
    if not movs:
        return None
    menor = movs[0]
    idx_menor = 0
    for i, m in enumerate(movs):
        if m.fe < menor.fe:
            menor = m
            idx_menor = i
    return movs.pop(idx_menor)


# Inicializa início e fim
inicio = None
final = None
for i in range(len(labirinto)):
    for j in range(len(labirinto[0])):
        if labirinto[i][j] == "C":
            inicio = Node(i, j, "C", poder=0)
        elif labirinto[i][j] == "S":
            final = Node(i, j, "S")

# Variáveis do algoritmo A*
movimentos = [inicio]
visitados = set()

# Para animação
passos = []  # registros das ações para animação (tipo, x, y, info)

# Execução do A*
while movimentos:
    atual = get_menor(movimentos)
    if (atual.indiceX, atual.indiceY, atual.poder) in visitados:
        continue
    visitados.add((atual.indiceX, atual.indiceY, atual.poder))
    passos.append(("visitado", atual.indiceX, atual.indiceY))

    if atual.indiceX == final.indiceX and atual.indiceY == final.indiceY:
        final = atual
        break

    filhos = []
    for dx, dy in direcoes:
        filho = Node(atual.indiceX + dx, atual.indiceY + dy, poder=atual.poder)
        filho.caminho = atual.caminho + [(atual.indiceX, atual.indiceY)]

        if validar_movimento(labirinto, filho, filho.poder):
            filho.letra = labirinto[filho.indiceX][filho.indiceY]
            if filho.letra == "F":
                filho.poder = 1
            if filho.letra == "A":
                filho.distancia_percorrida = (
                    atual.distancia_percorrida
                    + verifica_dist_percorrida(atual, filho)
                    + 1
                )
            else:
                filho.distancia_percorrida = (
                    atual.distancia_percorrida + verifica_dist_percorrida(atual, filho)
                )
            filho.fe = funcao_heuristica(filho, final)
            filhos.append(filho)
            passos.append(("gerado", filho.indiceX, filho.indiceY, filho.fe))
    movimentos.extend(filhos)

if final.indiceX == -1:
    print("Caminho não encontrado")
else:
    caminho_completo = final.caminho + [(final.indiceX, final.indiceY)]
    print("Caminho encontrado:", caminho_completo)


# Interface minimalista e funcional
class LabirintoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Labirinto A* - Minimalista")
        self.master.geometry("700x600")
        self.lab_frame = Frame(master)
        self.lab_frame.pack(pady=10)

        # Cores base
        self.cores = {
            "C": "#A8E6CF",
            "S": "#FF8B94",
            "A": "#AECBFA",
            "F": "#FFFACD",
            "B": "#6A6A6A",
            "_": "#FFFFFF",
        }
        self.labels = {}

        # Criação dos labels para o labirinto
        for i, row in enumerate(labirinto):
            for j, val in enumerate(row):
                cor = self.cores.get(val, "white")
                lbl = Label(
                    self.lab_frame,
                    text=val if val != "_" else " ",
                    width=4,
                    height=2,
                    bg=cor,
                    font=("Consolas", 16, "bold"),
                    relief="ridge",
                    borderwidth=1,
                )
                lbl.grid(row=i, column=j)
                self.labels[(i, j)] = lbl

        # Informações do estado
        self.info_frame = Frame(master)
        self.info_frame.pack(pady=5, fill=X)

        self.status_label = Label(
            self.info_frame, text="Status do algoritmo:", font=("Arial", 14)
        )
        self.status_label.pack(anchor="w")

        self.pos_label = Label(
            self.info_frame, text="Posição atual: -", font=("Arial", 12)
        )
        self.pos_label.pack(anchor="w")

        self.fe_label = Label(self.info_frame, text="FE atual: -", font=("Arial", 12))
        self.fe_label.pack(anchor="w")

        self.poder_label = Label(
            self.info_frame, text="Poder ativo: 0", font=("Arial", 12)
        )
        self.poder_label.pack(anchor="w")

        self.movimentos_label = Label(
            self.info_frame, text="Próximos movimentos (FE): -", font=("Arial", 12)
        )
        self.movimentos_label.pack(anchor="w")

        self.caminho_label = Label(
            self.info_frame, text="Caminho até agora: -", font=("Arial", 12)
        )
        self.caminho_label.pack(anchor="w")

        # Botão para iniciar animação
        self.btn_start = Button(
            master, text="Iniciar Animação", command=self.iniciar_animacao
        )
        self.btn_start.pack(pady=10)

        self.animacao_passos = passos.copy()
        self.movimentos_atuais = []
        self.personagem_pos = None
        self.animando_caminho = False

    def iniciar_animacao(self):
        self.movimentos = [inicio]
        self.visitados = set()
        self.personagem_pos = (inicio.indiceX, inicio.indiceY)
        self.atual = inicio
        self.movimentos_atuais = []
        self.animando_caminho = False
        self._animar_proximo_passo()

    def _animar_proximo_passo(self):
        if self.animando_caminho:
            self._animar_caminho_completo()
            return

        if not self.movimentos:
            # Quando acabar os movimentos, anima o caminho final
            self.animando_caminho = True
            self._animar_caminho_completo()
            return

        # Escolhe menor nó FE
        atual = get_menor(self.movimentos)
        if (atual.indiceX, atual.indiceY, atual.poder) in self.visitados:
            self.master.after(300, self._animar_proximo_passo)
            return

        self.visitados.add((atual.indiceX, atual.indiceY, atual.poder))
        self.atual = atual
        self.personagem_pos = (atual.indiceX, atual.indiceY)

        # Atualiza visual do personagem
        self._atualiza_visual_labirinto(atual)

        # Atualiza infos na tela
        self.pos_label.config(
            text=f"Posição atual: ({atual.indiceX}, {atual.indiceY}) [{labirinto[atual.indiceX][atual.indiceY]}]"
        )
        self.fe_label.config(text=f"FE atual: {atual.fe:.2f}")
        self.poder_label.config(text=f"Poder ativo: {atual.poder}")

        # Gera filhos e adiciona movimentos
        filhos = []
        filhos_texto = []
        for dx, dy in direcoes:
            filho = Node(atual.indiceX + dx, atual.indiceY + dy, poder=atual.poder)
            filho.caminho = atual.caminho + [(atual.indiceX, atual.indiceY)]

            if validar_movimento(labirinto, filho, filho.poder):
                filho.letra = labirinto[filho.indiceX][filho.indiceY]
                if filho.letra == "F":
                    filho.poder = 1
                if filho.letra == "A":
                    filho.distancia_percorrida = (
                        atual.distancia_percorrida
                        + verifica_dist_percorrida(atual, filho)
                        + 1
                    )
                else:
                    filho.distancia_percorrida = (
                        atual.distancia_percorrida
                        + verifica_dist_percorrida(atual, filho)
                    )
                filho.fe = funcao_heuristica(filho, final)
                filhos.append(filho)
                filhos_texto.append(
                    f"({filho.indiceX},{filho.indiceY}): FE={filho.fe:.2f}"
                )

        self.movimentos.extend(filhos)
        self.movimentos_atuais = filhos_texto
        self.movimentos_label.config(
            text=(
                "Próximos movimentos (FE): " + ", ".join(filhos_texto)
                if filhos_texto
                else "Nenhum"
            )
        )

        # Atualiza caminho até aqui
        caminho_txt = " -> ".join(
            [f"({x},{y})" for x, y in atual.caminho + [(atual.indiceX, atual.indiceY)]]
        )
        self.caminho_label.config(text=f"Caminho até agora: {caminho_txt}")

        if atual.indiceX == final.indiceX and atual.indiceY == final.indiceY:
            # Encontrou saída, anima caminho final
            self.animando_caminho = True
            self.caminho_final = atual.caminho + [(atual.indiceX, atual.indiceY)]
            self.master.after(600, self._animar_caminho_completo)
        else:
            self.master.after(600, self._animar_proximo_passo)

    def _atualiza_visual_labirinto(self, atual):
        # Resetar cores padrões
        for (i, j), lbl in self.labels.items():
            val = labirinto[i][j]
            cor = self.cores.get(val, "white")
            lbl.config(bg=cor, text=val if val != "_" else " ")

        # Destacar visitados
        for x, y, p in self.visitados:
            if (x, y) != (atual.indiceX, atual.indiceY):
                self.labels[(x, y)].config(bg="#D3D3D3")  # cinza claro

        # Destacar personagem atual
        self.labels[(atual.indiceX, atual.indiceY)].config(bg="#3399FF", text="😃")

    def _animar_caminho_completo(self):
        if not hasattr(self, "caminho_final") or not self.caminho_final:
            return
        if not hasattr(self, "idx_caminho"):
            self.idx_caminho = 0

        if self.idx_caminho >= len(self.caminho_final):
            self.status_label.config(text="Status do algoritmo: Caminho encontrado!")
            self.idx_caminho = 0
            return

        x, y = self.caminho_final[self.idx_caminho]

        # Reset cores
        for (i, j), lbl in self.labels.items():
            val = labirinto[i][j]
            cor = self.cores.get(val, "white")
            lbl.config(bg=cor, text=val if val != "_" else " ")

        # Destacar caminho final
        for pos in self.caminho_final:
            self.labels[pos].config(bg="#7FFF00")  # verde limão

        # Destacar personagem no caminho
        self.labels[(x, y)].config(bg="#3399FF", text="😃")

        self.pos_label.config(text=f"Posição atual: ({x}, {y}) - Caminho final")
        self.fe_label.config(text=f"Distância total: {final.distancia_percorrida:.2f}")
        self.poder_label.config(
            text=f"Poder ativo: {'Sim' if any(labirinto[i][j]=='F' for i,j in self.caminho_final) else 'Não'}"
        )
        self.movimentos_label.config(text="Próximos movimentos (FE): -")
        self.caminho_label.config(
            text=f"Caminho completo: {' -> '.join(str(p) for p in self.caminho_final)}"
        )

        self.idx_caminho += 1
        self.master.after(500, self._animar_caminho_completo)


root = Tk()
LabirintoGUI(root)
root.mainloop()
