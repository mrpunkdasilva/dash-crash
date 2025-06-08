import pygame
import random
from config.settings import WIDTH, HEIGHT

def draw_menu_background(screen, time=0, stars_count=50):
    """
    Desenha o fundo com gradiente e estrelas, igual ao menu.
    Pode ser usado tanto no menu quanto no jogo para consistência visual.
    """
    # Gradiente mais contrastante
    top_color = (20, 30, 60)  # Azul escuro no topo
    bottom_color = (80, 10, 120)  # Roxo escuro na base
    for y in range(0, HEIGHT, 2):
        ratio = y / HEIGHT
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        color = (r, g, b)
        pygame.draw.line(screen, color, (0, y), (WIDTH, y), 2)
    # Efeito de estrelas
    random.seed(int(time * 1000))  # Para animar as estrelas de forma sutil
    for _ in range(stars_count):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.uniform(0.5, 2)
        brightness = random.randint(180, 255)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)
