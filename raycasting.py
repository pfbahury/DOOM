import pygame
import sys
import math

# consts
WIN_HEIGHT = 480
WIN_WIDTH = WIN_HEIGHT * 2
MAP_SIZE = 8 # Mapa é 8x8
TILE_SIZE = int((WIN_HEIGHT / MAP_SIZE))
FOV = math.pi/3
HFOV = FOV/2
RAYS = 120
STEP_ANGLE = FOV/RAYS
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
ESCALA = (WIN_WIDTH/2)/RAYS

print(MAX_DEPTH)
# Var
# Coordenadas do "Jogador"
player_x = (WIN_WIDTH/2)/2 
player_y = (WIN_WIDTH/2)/2
player_angle = math.pi #direção que o player estiver olhando

# Dimensões do mapa
MAPA = (
    '########'
    '# #    #'
    '#    # #'
    '#      #'
    '#      #'
    '##     #'
    '#    # #'
    '########'
)



# iniciar pygame
pygame.init()

# Tela do Jogo
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # metade da tela 2d e outra metade 3d

# Titulo da tela
pygame.display.set_caption('DOOM (confia)')

# Init Timer
clock = pygame.time.Clock()

# Desenhar Mapa
def d_map():
    # Loop pelas linhas do mapa
    for row in range(MAP_SIZE):
        # Loop pelas colunas do mapa
        for col in range(MAP_SIZE):
            # Indice 
            indice_quadrado = (row* MAP_SIZE) + col

            # Desenhar o mapa dentro da tela 
            pygame.draw.rect(
                win,
                (200, 200, 200) if MAPA[indice_quadrado] == '#' else (100, 100, 100),
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
            )
    # Desenhar Player na interface 2D
    pygame.draw.circle(win, (255, 0, 0),
                       (int(player_x),
                        int(player_y)),
                        MAP_SIZE)

    # Direção do Player
    pygame.draw.line(win, (0, 255, 0),
                    (player_x, player_y),
                    (player_x - math.sin(player_angle) * 50,
                    player_y + math.cos(player_angle) * 50),
                    3)

    # Angulo maxímo esquerdo
    pygame.draw.line(win, (0, 255, 0),
                    (player_x, player_y),
                    (player_x - math.sin(player_angle - HFOV) * 50,
                    player_y + math.cos(player_angle - HFOV) * 50),
                    3)
    
    # Angulo maximo direito
    pygame.draw.line(win, (0, 255, 0),
                    (player_x, player_y),
                    (player_x - math.sin(player_angle + HFOV) * 50,
                    player_y + math.cos(player_angle + HFOV) * 50),
                    3)
    
# raycasting
def cast_rays():
    # Definir angulo maximo para a esquerda
    start_angle = player_angle - HFOV
    # Loop de RAYS
    for ray in range(RAYS):
        # adicionar raios de visão a cada loop
        for depth in range(MAX_DEPTH):
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth

            # Usamos os targets da visão para definir o numero de colunas e linhas
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)

            # Calculamos novamente o indice quadrado
            indice_quadrado = row * MAP_SIZE + col

            # Se os raios atingirem os limites do mapa
            if MAPA[indice_quadrado] == '#':
                # trocar a cor da parede atingida pelo campo de visão
                pygame.draw.rect(win, (0,255,0), (col * TILE_SIZE,
                                                 row * TILE_SIZE,
                                                 TILE_SIZE - 2,
                                                 TILE_SIZE - 2))

                pygame.draw.line(win, (255,255,0),
                                (player_x, player_y),
                                (target_x, target_y))
                
                # colorir parede
                cor = 255 / (1 + depth * depth * 0.0001)
                
                # Mudar efeito de visão
                depth *= math.cos(player_angle - start_angle)

                # Tamanho da parede
                wall_height = 21000 / (depth + 0.0001)

                # impedir de ficar preso na parede
                if wall_height > WIN_HEIGHT:
                    wall_height = WIN_HEIGHT

                # desenhar projeção 3D
                pygame.draw.rect(win, (cor, cor, cor), (
                    WIN_HEIGHT + ray * ESCALA,
                    (WIN_HEIGHT/2) - wall_height / 2,
                    ESCALA, wall_height
                ))
                break #linha se quebra ao acertar uma parede
        # Incrementar cada linha de FOV
        start_angle += STEP_ANGLE


forward = True
# Loop
while True:
    # condição de escape
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    # Usamos os targets da visão para definir o numero de colunas e linhas
    col = int(player_x/TILE_SIZE)
    row = int(player_y/TILE_SIZE)

    # Calculamos novamente o indice quadrado
    indice_quadrado = row * MAP_SIZE + col

    # Se os player atingir o limites do mapa
    if MAPA[indice_quadrado] == '#':
        if forward:
            player_x -= -math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:
            player_x += -math.sin(player_angle) * 5
            player_y += math.cos(player_angle) * 5


    # background 2D
    pygame.draw.rect(win, (0,0,0), (0,0,WIN_HEIGHT, WIN_HEIGHT))
    
    # background 3D
    pygame.draw.rect(win, (100,100,100),
                    (480, WIN_HEIGHT/2,
                    WIN_HEIGHT,
                    WIN_HEIGHT))
    pygame.draw.rect(win, (200,200,200),
                    (480, -WIN_HEIGHT/2,
                    WIN_HEIGHT,
                    WIN_HEIGHT))

    # Desenhar o mapa
    d_map()

    # raycast
    cast_rays()


    # controles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player_angle -= 0.1
    if keys[pygame.K_RIGHT]: player_angle += 0.1
    if keys[pygame.K_UP]:
        forward = True
        player_x += -math.sin(player_angle) * 5
        player_y += math.cos(player_angle) * 5
    if keys[pygame.K_DOWN]:
        forward = False
        player_x -= -math.sin(player_angle) * 5
        player_y -= math.cos(player_angle) * 5
    
    # FPS
    clock.tick(45)
    # update display
    pygame.display.flip()