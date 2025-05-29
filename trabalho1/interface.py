import tkinter as tk
import time
from a_star import executar_busca
from PIL import Image, ImageTk

CELL_SIZE = 100


def carregar_matriz(arquivo):
    matriz = []
    with open(arquivo, "r") as f:
        for linha in f:
            matriz.append(linha.strip().split())
    return matriz


def carregar_imagens(master):
    letras = ["B", "F", "A", "C", "S"]
    imagens = {}
    for letra in letras:
        img = Image.open(f"img/{letra}.png").resize((CELL_SIZE, CELL_SIZE))
        imagens[letra] = ImageTk.PhotoImage(img, master=master)
    return imagens


def desenhar_labirinto(canvas, matriz, imagens):
    objetos_canvas = []
    for i, linha in enumerate(matriz):
        linha_obj = []
        for j, celula in enumerate(linha):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            if celula == "_":
                rect = canvas.create_rectangle(
                    x,
                    y,
                    x + CELL_SIZE,
                    y + CELL_SIZE,
                    fill="white",
                    outline="lightgray",
                )
                linha_obj.append(None)
            else:
                img = imagens.get(celula)
                item = canvas.create_image(x, y, anchor=tk.NW, image=img)
                linha_obj.append(item)
        objetos_canvas.append(linha_obj)
    return objetos_canvas


def animar_caminho(
    canvas, historico, caminho_final, personagem_img, matriz, objetos_canvas
):
    personagem = None
    marcador_fe = []
    poder_fruta = False
    barreira_destruida = False

    for passo in historico:
        x, y = passo["pos"]

        # Atualiza fe dos filhos
        for m in marcador_fe:
            canvas.delete(m)
        marcador_fe.clear()
        for fx, fy, fe in passo["filhos"]:
            cx = fy * CELL_SIZE + 30
            cy = fx * CELL_SIZE + 70

            texto_explicativo = f"FE: {fe:.1f}"
            largura_texto = len(texto_explicativo) * 6  # estimativa
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

        # Atualiza personagem
        if personagem:
            canvas.delete(personagem)
        personagem = canvas.create_image(
            y * CELL_SIZE, x * CELL_SIZE, anchor=tk.NW, image=personagem_img
        )
        canvas.update()
        time.sleep(1.0)

    if personagem:
        canvas.delete(personagem)
    personagem = canvas.create_image(
        caminho_final[0][1] * CELL_SIZE,
        caminho_final[0][0] * CELL_SIZE,
        anchor=tk.NW,
        image=personagem_img,
    )
    canvas.update()
    time.sleep(0.4)

    for i in range(1, len(caminho_final)):
        x0, y0 = caminho_final[i - 1]
        x1, y1 = caminho_final[i]

        canvas.create_line(
            y0 * CELL_SIZE + CELL_SIZE // 2,
            x0 * CELL_SIZE + CELL_SIZE // 2,
            y1 * CELL_SIZE + CELL_SIZE // 2,
            x1 * CELL_SIZE + CELL_SIZE // 2,
            fill="red",
            width=4,
        )

        # Move o personagem para o próximo passo
        canvas.delete(personagem)
        personagem = canvas.create_image(
            y1 * CELL_SIZE, x1 * CELL_SIZE, anchor=tk.NW, image=personagem_img
        )
        canvas.update()
        time.sleep(0.4)


def iniciar_interface():
    matriz = carregar_matriz("labirinto.txt")

    root = tk.Tk()
    root.title("Algoritmo A* - Animação com Objetos")
    root.configure(bg="white")  # Fundo da janela

    imagens = carregar_imagens(root)
    caminho, distancia, historico = executar_busca(matriz)

    canvas = tk.Canvas(
        root,
        width=len(matriz[0]) * CELL_SIZE,
        height=len(matriz) * CELL_SIZE,
        bg="white",
    )
    canvas.pack(padx=20, pady=20)

    objetos_canvas = desenhar_labirinto(canvas, matriz, imagens)

    if caminho:
        print(f"Caminho encontrado! Distância total: {distancia:.2f}")
        print("Caminho:", caminho)
        personagem_img = ImageTk.PhotoImage(
            Image.open("img/personagem.png").resize((CELL_SIZE, CELL_SIZE)), master=root
        )
        root.after(
            1000,
            lambda: animar_caminho(
                canvas, historico, caminho, personagem_img, matriz, objetos_canvas
            ),
        )
    else:
        print("Caminho não encontrado.")

    root.mainloop()


if __name__ == "__main__":
    iniciar_interface()
