# Labirinto A* - Algoritmo de Busca com Visualização Gráfica

**Trabalho Prático 1 - IA**

Um projeto educacional que implementa o algoritmo **A*** (A-Star) para resolver labirintos com obstáculos dinâmicos, poderes especiais e custos variáveis. Inclui uma interface gráfica interativa que visualiza o processo de busca em tempo real.

## 📋 Descrição

Este projeto demonstra a implementação do algoritmo de busca A*, um algoritmo clássico de inteligência artificial que combina as vantagens da busca de custo uniforme e da busca gulosa. O programa encontra o caminho mais curto de um ponto inicial até um ponto final em um labirinto, considerando:

- **Obstáculos (B)**: Barreiras que bloqueiam o caminho
- **Poderes (F)**: Frutas que permitem atravessar barreiras
- **Terrenos com custo (A)**: Áreas que aumentam o custo de movimento
- **Movimento em 8 direções**: Horizontal, vertical e diagonal

## 🗺️ Símbolos do Labirinto

| Símbolo | Descrição | Efeito |
|---------|-----------|--------|
| **C** | Começo | Posição inicial de busca |
| **S** | Saída | Objetivo final |
| **B** | Barreira | Obstáculo (intransponível sem poder) |
| **F** | Fruta/Poder | Ativa capacidade de atravessar barreiras |
| **A** | Área de risco | Terreno com custo extra de movimento (+1) |
| **_** | Espaço vazio | Caminho livre (custo: 1) |

## 🚀 Como Usar

### Pré-requisitos

```bash
pip install pillow
```

### Execução

```bash
python interface.py
```

A interface gráfica abrirá automaticamente com uma animação do algoritmo A* resolvendo o labirinto.

### Personalizando Labirintos

1. Edite o arquivo `labirinto.txt` ou crie um novo
2. Use o formato: caracteres separados por espaços, uma linha por linha do labirinto
3. Inclua exatamente um `C` (começo) e um `S` (saída)
4. Para carregar um labirinto diferente, modifique a linha em `interface.py`:
   ```python
   matriz = carregar_matriz("seu_labirinto.txt")
   ```

## 📊 Algoritmo A*

O algoritmo utiliza a fórmula:
```
f(n) = g(n) + h(n)

Onde:
- f(n) = custo total estimado
- g(n) = distância percorrida até o nó
- h(n) = heurística (distância em linha reta até o objetivo)
```

### Custos de Movimento

- **Movimento reto** (horizontal/vertical): 1
- **Movimento diagonal**: √2 ≈ 1.414
- **Célula com tipo 'A'**: +1 adicional

### Heurística

Usa **distância euclidiana** do nó atual até o objetivo:
```python
h(n) = √[(x_atual - x_objetivo)² + (y_atual - y_objetivo)²]
```

## 📊 Saída

Após a execução, o programa exibe no console:
- Caminho encontrado (lista de coordenadas)
- Distância total percorrida
- Indicação se o caminho foi ou não encontrado

## 🎨 Imagens Necessárias

O projeto requer imagens PNG na pasta `img/`:
- `C.png` - Ícone de começo
- `S.png` - Ícone de saída
- `B.png` - Ícone de barreira
- `F.png` - Ícone de fruta/poder
- `A.png` - Ícone de área de risco
- `personagem.png` - Ícone do personagem/agente

## 🔬 Complexidade

- **Complexidade de Tempo**: O(b^d) onde b é o fator de ramificação e d é a profundidade
- **Complexidade de Espaço**: O(b^d)
- **Admissibilidade**: Garantida com heurística admissível (distância euclidiana)
