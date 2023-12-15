import pygame
import sys
import heapq

# Inicialização do Pygame
pygame.init()

# Definição de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Tamanho da janela
WIDTH, HEIGHT = 400, 400

# Função para desenhar o grafo
def draw_graph(screen, graph, fixed_numbers, current_node):
    screen.fill(WHITE)

    # Desenha arestas
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            pygame.draw.line(screen, BLACK, node_positions[node], node_positions[neighbor], 2)
            # Desenha o peso da aresta (em vermelho)
            font = pygame.font.Font(None, 20)
            text = font.render(str(weight), True, (255, 0, 0))
            text_rect = text.get_rect(center=((node_positions[node][0] + node_positions[neighbor][0]) // 2,
                                              (node_positions[node][1] + node_positions[neighbor][1]) // 2))
            screen.blit(text, text_rect)

    # Desenha nós
    for node, pos in node_positions.items():
        pygame.draw.circle(screen, RED if node == current_node else GREEN, pos, 20)

        # Desenha o número fixo no nó
        font = pygame.font.Font(None, 24)
        text = font.render(str(fixed_numbers[node]), True, BLACK)
        screen.blit(text, (pos[0] - 10, pos[1] - 10))

    pygame.display.flip()

# Função principal do algoritmo de Dijkstra
def dijkstra_animation(graph, start):
    fixed_numbers = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}

    while True:
        distances = {node: float('infinity') for node in graph}
        distances[start] = 0
        queue = [(0, start)]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))

            draw_graph(screen, graph, fixed_numbers, current_node)
            pygame.time.delay(500)  # Adiciona um atraso para a visualização

# Definição do grafo e das posições dos nós
graph = {
    'A': {'B': 5, 'C': 4, 'E': 7},
    'B': {'A': 5, 'C': 2, 'D': 5, 'E': 8},
    'C': {'A': 4, 'B': 2, 'D': 1, 'E': 2},
    'D': {'B': 5, 'C': 1, 'E': 3},
    'E': {'A': 7, 'B': 8, 'C': 2, 'D': 3, 'F': 4},
    'F': {'E': 4}
}

node_positions = {
    'A': (50, 50),
    'B': (150, 50),
    'C': (150, 150),
    'D': (250, 150),
    'E': (50, 250),
    'F': (150, 250)
}

# Inicialização da janela Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dijkstra Animation')

# Loop externo da animação
while True:
    dijkstra_animation(graph, 'A')
