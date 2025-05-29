import tkinter as tk
import time
from a_star import executar_busca  # Importa a função principal de busca A*
from PIL import Image, ImageTk  # Para carregar e redimensionar imagens

CELL_SIZE = 100  # Tamanho de cada célula no labirinto


# Carrega a matriz do labirinto a partir de um arquivo de texto
def carregar_matriz(arquivo):
    matriz = []
    with open(arquivo, "r") as f:
        for linha in f:
            matriz.append(linha.strip().split())  # Divide cada linha em células
    return matriz


# Carrega as imagens das letras usadas no labirinto
def carregar_imagens(master):
    letras = ["B", "F", "A", "C", "S"]
    imagens = {}
    for letra in letras:
        img = Image.open(f"img/{letra}.png").resize(
            (CELL_SIZE - 2, CELL_SIZE - 2)
        )  # 2 pixels de margem
        imagens[letra] = ImageTk.PhotoImage(
            img, master=master
        )  # Salva com referência à janela
    return imagens


# Desenha o labirinto na tela com base na matriz e imagens
def desenhar_labirinto(canvas, matriz, imagens):
    objetos_canvas = []  # Guarda os objetos desenhados
    for i, linha in enumerate(matriz):
        linha_obj = []
        for j, celula in enumerate(linha):
            x = j * CELL_SIZE
            y = i * CELL_SIZE

            # Desenha a linha da célula
            canvas.create_rectangle(
                x, y, x + CELL_SIZE, y + CELL_SIZE, fill="white", outline="gray30"
            )

            # Se a célula tem imagem (como 'B', 'F', etc), desenha
            if celula in imagens:
                img = imagens[celula]
                item = canvas.create_image(
                    x + 1, y + 1, anchor=tk.NW, image=img
                )  # deslocamento para a imagem caber dentro do quadrado
                linha_obj.append(item)
            else:
                linha_obj.append(None)
        objetos_canvas.append(linha_obj)
    return objetos_canvas


# Faz a animação da movimentação do personagem e das marcações no labirinto
def animar_caminho(
    canvas, historico, caminho_final, personagem_img, matriz, objetos_canvas
):
    personagem = None
    marcador_fe = []  # Guarda os marcadores "FE" visuais
    poder_fruta = False  # Flag para indicar se o personagem pegou a fruta
    barreira_destruida = False  # Flag para indicar se já destruiu a barreira

    for passo in historico:
        x, y = passo["pos"]

        # Apaga marcadores antigos
        for m in marcador_fe:
            canvas.delete(m)
        marcador_fe.clear()

        # Exibe FE dos filhos gerados nesse passo
        for fx, fy, fe in passo["filhos"]:
            cx = fy * CELL_SIZE + 30
            cy = fx * CELL_SIZE + 70

            texto_explicativo = f"FE: {fe:.1f}"
            largura_texto = len(texto_explicativo) * 6  # Tamanho aproximado do texto

            # Caixa de fundo do texto
            fundo = canvas.create_rectangle(
                cx - 4,
                cy - 12,
                cx - 4 + largura_texto,
                cy + 10,
                fill="#f8f8f8",
                outline="gray",
            )
            texto = canvas.create_text(
                cx + largura_texto // 2 - 4,
                cy,
                text=texto_explicativo,
                fill="black",
                font=("Helvetica", 10, "bold"),
            )
            marcador_fe.extend([fundo, texto])

        # Remove fruta se pegar
        if matriz[x][y] == "F":
            if objetos_canvas[x][y]:
                canvas.delete(objetos_canvas[x][y])
                objetos_canvas[x][y] = None
            matriz[x][y] = "_"
            poder_fruta = True

        # Remove barreira se tiver poder e ainda não destruiu
        if matriz[x][y] == "B" and poder_fruta and not barreira_destruida:
            if objetos_canvas[x][y]:
                canvas.delete(objetos_canvas[x][y])
                objetos_canvas[x][y] = None
            matriz[x][y] = "_"
            barreira_destruida = True

        # Move o personagem
        if personagem:
            canvas.delete(personagem)
        personagem = canvas.create_image(
            y * CELL_SIZE, x * CELL_SIZE, anchor=tk.NW, image=personagem_img
        )
        canvas.update()
        time.sleep(2.0)  # Tempo de espera entre cada passo

    # Reposiciona personagem no início do caminho
    if personagem:
        canvas.delete(personagem)
    personagem = canvas.create_image(
        caminho_final[0][1] * CELL_SIZE,
        caminho_final[0][0] * CELL_SIZE,
        anchor=tk.NW,
        image=personagem_img,
    )
    canvas.update()
    time.sleep(0.5)

    # Anima o caminho completo com linha vermelha e personagem
    for i in range(1, len(caminho_final)):
        x0, y0 = caminho_final[i - 1]
        x1, y1 = caminho_final[i]

        # Linha vermelha entre os pontos para demonstração do caminho
        canvas.create_line(
            y0 * CELL_SIZE + CELL_SIZE // 2,
            x0 * CELL_SIZE + CELL_SIZE // 2,
            y1 * CELL_SIZE + CELL_SIZE // 2,
            x1 * CELL_SIZE + CELL_SIZE // 2,
            fill="red",
            width=4,
        )

        # Move o personagem
        canvas.delete(personagem)
        personagem = canvas.create_image(
            y1 * CELL_SIZE, x1 * CELL_SIZE, anchor=tk.NW, image=personagem_img
        )
        canvas.update()
        time.sleep(0.5)


# Função principal da interface gráfica
def iniciar_interface():
    matriz = carregar_matriz("labirinto.txt")  # Lê o labirinto do arquivo

    root = tk.Tk()
    root.title("Algoritmo A* - Animação com Objetos")
    root.configure(bg="white")  # Fundo da janela

    imagens = carregar_imagens(root)  # Carrega imagens usadas no mapa

    # Cria o canvas de desenho do labirinto
    canvas = tk.Canvas(
        root,
        width=len(matriz[0]) * CELL_SIZE,
        height=len(matriz) * CELL_SIZE,
        bg="white",
    )
    canvas.pack(padx=20, pady=20)

    objetos_canvas = desenhar_labirinto(canvas, matriz, imagens)

    # Função chamada ao clicar no botão "Reiniciar"
    def iniciar_animacao():
        caminho, distancia, historico = executar_busca(matriz)
        canvas.delete("all")  # Limpa o canvas
        nonlocal objetos_canvas
        objetos_canvas = desenhar_labirinto(canvas, matriz, imagens)  # Redesenha
        if caminho:
            print(f"Caminho encontrado! Distância total: {distancia:.2f}")
            print("Caminho:", caminho)
            personagem_img = ImageTk.PhotoImage(
                Image.open("img/personagem.png").resize((CELL_SIZE - 2, CELL_SIZE - 2)),
                master=root,
            )
            animar_caminho(
                canvas, historico, caminho, personagem_img, matriz, objetos_canvas
            )
        else:
            print("Caminho não encontrado.")

    btn_reiniciar = tk.Button(root, text="Reiniciar", command=iniciar_animacao)
    btn_reiniciar.pack(pady=10)

    iniciar_animacao()  # Executa a animação automaticamente ao iniciar

    root.mainloop()


# Executa o programa se este arquivo for o principal
if __name__ == "__main__":
    iniciar_interface()
