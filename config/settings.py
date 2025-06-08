# Configurações do jogo
import pygame
import os

# Dimensões da tela
WIDTH = 1000
HEIGHT = 600

# Paleta de cores moderna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (50, 50, 50)

# Cores primárias
RED = (235, 77, 75)
BLUE = (74, 105, 189)
GREEN = (85, 230, 100)
YELLOW = (253, 203, 110)
ORANGE = (250, 152, 58)
PURPLE = (165, 94, 234)
CYAN = (72, 219, 251)
PINK = (255, 107, 129)

# Cores de destaque
HIGHLIGHT_BLUE = (116, 185, 255)
HIGHLIGHT_GREEN = (162, 255, 134)
HIGHLIGHT_RED = (255, 118, 117)
HIGHLIGHT_YELLOW = (254, 223, 0)

# Cores de fundo
BG_DARK = (44, 62, 80)
BG_LIGHT = (236, 240, 241)
BG_BLUE = (30, 55, 153)
BG_GREEN = (46, 204, 113)

# Cores de interface
UI_PRIMARY = (52, 73, 94)
UI_SECONDARY = (72, 126, 176)
UI_ACCENT = (26, 188, 156)
UI_TEXT = (236, 240, 241)
UI_WARNING = (241, 196, 15)
UI_DANGER = (231, 76, 60)
UI_SUCCESS = (46, 204, 113)

# Configurações de jogo
FPS = 60
PARTICLE_COUNT = 20
TRAIL_LENGTH = 10

# Caminhos para recursos
FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'fonts')

# Inicialização de fontes
def init_fonts():
    pygame.font.init()
    
    # Tenta carregar fontes personalizadas se disponíveis, senão usa as do sistema
    try:
        title_font = pygame.font.Font(os.path.join(FONT_DIR, 'title_font.ttf'), 36)
    except:
        title_font = pygame.font.SysFont("Arial", 36)
        
    try:
        heading_font = pygame.font.Font(os.path.join(FONT_DIR, 'heading_font.ttf'), 30)
    except:
        heading_font = pygame.font.SysFont("Arial", 30)
    
    return {
        "title": title_font,
        "heading": heading_font,
        "large": pygame.font.SysFont("Arial", 30, bold=True),
        "medium": pygame.font.SysFont("Arial", 24),
        "small": pygame.font.SysFont("Arial", 20),
        "tiny": pygame.font.SysFont("Arial", 16)
    }