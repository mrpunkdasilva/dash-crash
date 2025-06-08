import pygame
import math
import random
from config.settings import BLUE, BLACK, YELLOW, RED, HIGHLIGHT_BLUE, DARK_GRAY, WHITE, ORANGE, CYAN, LIGHT_GRAY

class Car:
    def __init__(self, x=0, speed=2.0, max_speed=8.0, color=BLUE):
        self.x = x
        self.y = 0  # Será calculado com base na função da pista
        self.speed = speed
        self.max_speed = max_speed
        self.color = color
        self.crashed = False
        self.surface = self._create_surface(color)
        self.trail = []  # Rastro do carro
        self.max_trail_length = 15
        self.exhaust_particles = []  # Partículas de escapamento
        
    def _create_surface(self, color):
        """Cria a superfície do carro com a cor especificada e design melhorado"""
        # Cria uma superfície maior para mais detalhes
        car = pygame.Surface((80, 40), pygame.SRCALPHA)
        
        # Cores derivadas da cor principal para efeitos de sombreamento
        darker_color = (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40))
        lighter_color = (min(255, color[0] + 40), min(255, color[1] + 40), min(255, color[2] + 40))
        
        # Corpo principal do carro (com formato mais aerodinâmico)
        # Desenha o corpo principal com gradiente
        for i in range(60):
            blend_factor = i / 60.0
            current_color = (
                int(color[0] * (1 - blend_factor) + lighter_color[0] * blend_factor),
                int(color[1] * (1 - blend_factor) + lighter_color[1] * blend_factor),
                int(color[2] * (1 - blend_factor) + lighter_color[2] * blend_factor)
            )
            pygame.draw.line(car, current_color, (10 + i, 8), (10 + i, 28), 1)
        
        # Contorno do carro
        points = [(8, 18), (15, 8), (65, 8), (70, 18), (65, 28), (15, 28)]
        pygame.draw.polygon(car, darker_color, points)
        pygame.draw.polygon(car, color, points, 1)
        
        # Detalhes do corpo
        highlight_color = HIGHLIGHT_BLUE if color == BLUE else YELLOW if color == RED else WHITE
        
        # Faixa decorativa no topo
        pygame.draw.line(car, highlight_color, (15, 9), (65, 9), 2)
        
        # Faixa decorativa na lateral
        pygame.draw.line(car, darker_color, (10, 18), (70, 18), 2)
        
        # Rodas com mais detalhes
        wheel_color = BLACK
        wheel_highlight = LIGHT_GRAY
        
        # Roda frontal esquerda
        pygame.draw.ellipse(car, wheel_color, (12, 2, 16, 8))
        pygame.draw.ellipse(car, wheel_highlight, (15, 4, 6, 3))
        
        # Roda traseira esquerda
        pygame.draw.ellipse(car, wheel_color, (52, 2, 16, 8))
        pygame.draw.ellipse(car, wheel_highlight, (55, 4, 6, 3))
        
        # Roda frontal direita
        pygame.draw.ellipse(car, wheel_color, (12, 30, 16, 8))
        pygame.draw.ellipse(car, wheel_highlight, (15, 32, 6, 3))
        
        # Roda traseira direita
        pygame.draw.ellipse(car, wheel_color, (52, 30, 16, 8))
        pygame.draw.ellipse(car, wheel_highlight, (55, 32, 6, 3))
        
        # Faróis com brilho
        # Farol dianteiro
        pygame.draw.ellipse(car, YELLOW, (67, 14, 8, 8))
        pygame.draw.ellipse(car, WHITE, (69, 16, 4, 4))
        
        # Farol traseiro
        pygame.draw.ellipse(car, RED, (5, 14, 8, 8))
        pygame.draw.ellipse(car, (255, 150, 150), (7, 16, 4, 4))
        
        # Janelas com reflexo
        window_color = CYAN
        window_highlight = WHITE
        
        # Janela principal
        pygame.draw.rect(car, window_color, (25, 10, 30, 8), border_radius=3)
        
        # Reflexo na janela
        pygame.draw.line(car, window_highlight, (28, 12), (50, 12), 2)
        
        # Detalhes adicionais
        # Spoiler traseiro
        pygame.draw.rect(car, darker_color, (5, 13, 3, 10), border_radius=1)
        
        # Escapamento
        pygame.draw.rect(car, DARK_GRAY, (3, 17, 4, 3), border_radius=1)
        
        return car
        
    def update_position(self, track_function):
        """Atualiza a posição do carro"""
        if not self.crashed:
            # Atualiza a posição
            old_x, old_y = self.x, self.y
            self.x += self.speed
            self.y = track_function(self.x)
            
            # Atualiza o rastro
            self._update_trail(old_x, old_y)
            
            # Atualiza as partículas
            self._update_particles()
            
            # Gera novas partículas se o carro estiver em movimento
            if self.speed > 0.5:
                self._generate_particles()
    
    def _update_trail(self, old_x, old_y):
        """Atualiza o rastro do carro com mais pontos para um efeito mais suave"""
        if self.speed > 0.5:
            # Adiciona vários pontos entre a posição antiga e a nova para um rastro mais suave
            steps = 3  # Número de pontos intermediários
            for i in range(steps):
                # Interpola entre a posição antiga e a nova
                t = i / steps
                interp_x = old_x + (self.x - old_x) * t
                interp_y = old_y + (self.y - old_y) * t
                self.trail.append((interp_x, interp_y))
            
            # Limita o tamanho do rastro
            while len(self.trail) > self.max_trail_length:
                self.trail.pop(0)
    
    def _generate_particles(self):
        """Gera partículas de escapamento"""
        if random.random() < 0.3 * (self.speed / self.max_speed):
            # Posição inicial da partícula (atrás do carro)
            particle = {
                'x': self.x - 5,
                'y': self.y,
                'size': random.uniform(2, 4),
                'color': (
                    random.randint(200, 255),
                    random.randint(100, 150),
                    random.randint(0, 50)
                ),
                'life': random.uniform(0.5, 1.5),
                'max_life': random.uniform(0.5, 1.5),
                'dx': random.uniform(-1, -0.5) * self.speed,
                'dy': random.uniform(-0.5, 0.5)
            }
            self.exhaust_particles.append(particle)
    
    def _update_particles(self):
        """Atualiza as partículas de escapamento"""
        for particle in self.exhaust_particles[:]:
            # Atualiza a vida da partícula
            particle['life'] -= 0.05
            
            # Atualiza a posição
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Atualiza o tamanho e a transparência com base na vida
            life_ratio = particle['life'] / particle['max_life']
            particle['size'] *= 0.95
            # Atualiza apenas a cor RGB, sem alpha
            particle['color'] = (
                particle['color'][0],
                particle['color'][1],
                particle['color'][2]
            )
            
            # Remove partículas mortas
            if particle['life'] <= 0 or particle['size'] < 0.5:
                self.exhaust_particles.remove(particle)
            
    def set_crashed(self):
        """Define o carro como batido"""
        self.crashed = True
        self.speed = 0
        self.surface = self._create_surface(RED)
        
        # Gera muitas partículas na colisão
        for _ in range(20):
            particle = {
                'x': self.x + random.uniform(-10, 10),
                'y': self.y + random.uniform(-10, 10),
                'size': random.uniform(3, 7),
                'color': (
                    random.randint(200, 255),
                    random.randint(0, 100),
                    random.randint(0, 50)
                ),
                'life': random.uniform(1.0, 2.0),
                'max_life': random.uniform(1.0, 2.0),
                'dx': random.uniform(-2, 2),
                'dy': random.uniform(-2, 2)
            }
            self.exhaust_particles.append(particle)
        
    def reset(self, x=0, color=BLUE):
        """Reinicia o estado do carro"""
        self.x = x
        self.speed = 2.0
        self.crashed = False
        self.color = color
        self.surface = self._create_surface(color)
        self.trail = []
        self.exhaust_particles = []
        
    def get_rotated_surface(self, slope):
        """Retorna a superfície do carro rotacionada de acordo com a inclinação da pista"""
        angle = math.degrees(math.atan(-slope))
        return pygame.transform.rotate(self.surface, angle)
        
    def draw_effects(self, screen, camera_x, camera_y, height):
        """Desenha efeitos visuais do carro (rastro e partículas)"""
        # Desenha o rastro com efeito de desvanecimento e brilho
        if len(self.trail) > 1:
            points = []
            for i, (trail_x, trail_y) in enumerate(self.trail):
                points.append((trail_x - camera_x, height - (trail_y - camera_y)))
            
            if len(points) > 1:
                # Cores base para o rastro
                if isinstance(self.color, tuple) and len(self.color) >= 3:
                    base_color = (self.color[0], self.color[1], self.color[2])
                else:
                    base_color = BLUE
                
                # Cores para o efeito de rastro (mais vibrantes)
                glow_color = (min(255, base_color[0] + 50), 
                             min(255, base_color[1] + 50), 
                             min(255, base_color[2] + 50))
                
                # Desenha o rastro com largura variável e cores que desvanecem
                for i in range(len(points) - 1):
                    # Calcula a largura e a opacidade com base na posição no rastro
                    progress = i / (len(points) - 1)
                    width = max(1, int(5 * (1 - progress)))
                    alpha = int(200 * (1 - progress))
                    
                    # Interpola entre a cor de brilho e a cor base
                    r = int(glow_color[0] * (1 - progress) + base_color[0] * progress)
                    g = int(glow_color[1] * (1 - progress) + base_color[1] * progress)
                    b = int(glow_color[2] * (1 - progress) + base_color[2] * progress)
                    
                    # Cria uma superfície para a linha com transparência
                    line_length = int(((points[i][0] - points[i+1][0])**2 + 
                                      (points[i][1] - points[i+1][1])**2)**0.5)
                    line_surface = pygame.Surface((line_length, width), pygame.SRCALPHA)
                    
                    # Desenha a linha na superfície
                    pygame.draw.line(line_surface, (r, g, b, alpha), 
                                    (0, width//2), (line_length, width//2), width)
                    
                    # Calcula o ângulo da linha
                    dx = points[i+1][0] - points[i][0]
                    dy = points[i+1][1] - points[i][1]
                    angle = math.degrees(math.atan2(dy, dx))
                    
                    # Rotaciona a superfície
                    rotated_line = pygame.transform.rotate(line_surface, -angle)
                    
                    # Posiciona e desenha a linha
                    rect = rotated_line.get_rect(center=((points[i][0] + points[i+1][0])//2, 
                                                        (points[i][1] + points[i+1][1])//2))
                    screen.blit(rotated_line, rect)
        
        # Desenha as partículas
        for particle in self.exhaust_particles:
            particle_surface = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
            # Garante que a cor tenha apenas 3 componentes RGB
            color = particle['color']
            if isinstance(color, tuple) and len(color) > 3:
                color = color[:3]  # Pega apenas os componentes RGB
            pygame.draw.circle(
                particle_surface, 
                color, 
                (int(particle['size']), int(particle['size'])), 
                int(particle['size'])
            )
            screen.blit(
                particle_surface, 
                (particle['x'] - camera_x - particle['size'], 
                 height - (particle['y'] - camera_y) - particle['size'])
            )