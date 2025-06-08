import pygame
import random
import math
from config.settings import WIDTH, HEIGHT, BG_DARK, BG_LIGHT, BLUE, WHITE, YELLOW, ORANGE, CYAN
from src.models.car import Car

class Menu:
    def __init__(self, screen, fonts):
        """Inicializa o menu"""
        self.screen = screen
        self.fonts = fonts
        self.running = True

        # Fundo animado
        from src.views.animated_background import AnimatedBackground
        self.animated_bg = AnimatedBackground(n_stars=60, n_particles=0)
        
        # Inicializa o carro para o menu
        self.car = Car(x=WIDTH//2 - 100, speed=0, color=BLUE)
        self.car.y = HEIGHT - 150
        
        # Inicializa partículas de neve
        self.snow_particles = []
        self.generate_snow_particles(100)
        
        # Inicializa partículas de cálculos
        self.math_particles = []
        self.generate_math_particles(30)
        
        # Tempo para animações
        self.time = 0
        self.clock = pygame.time.Clock()

    def generate_snow_particles(self, count):
        """Gera partículas de neve para efeito visual"""
        for _ in range(count):
            self.snow_particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.uniform(1, 3),
                'speed': random.uniform(0.5, 2.0),
                'color': (
                    random.randint(220, 255),
                    random.randint(220, 255),
                    random.randint(220, 255)
                )
            })
    
    def generate_math_particles(self, count):
        """Gera partículas de cálculos para efeito visual"""
        math_symbols = ["∫", "∂", "∑", "√", "∞", "d/dx", "f'(x)", "∇", "∆", "∏"]
        for _ in range(count):
            self.math_particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'symbol': random.choice(math_symbols),
                'size': random.randint(14, 24),
                'speed': random.uniform(0.3, 1.0),
                'color': (
                    random.randint(150, 255),
                    random.randint(150, 255),
                    random.randint(150, 255)
                ),
                'rotation': random.uniform(0, 360)
            })
    
    def update_snow_particles(self):
        """Atualiza as partículas de neve"""
        for particle in self.snow_particles:
            # Move as partículas de neve
            particle['y'] += particle['speed']
            particle['x'] += math.sin(self.time * 0.5 + particle['y'] * 0.01) * 0.5
            
            # Reposiciona partículas que saem da tela
            if particle['y'] > HEIGHT:
                particle['y'] = 0
                particle['x'] = random.randint(0, WIDTH)
                
            if particle['x'] < 0:
                particle['x'] = WIDTH
            elif particle['x'] > WIDTH:
                particle['x'] = 0
    
    def update_math_particles(self):
        """Atualiza as partículas de cálculos"""
        for particle in self.math_particles:
            # Move as partículas de cálculos
            particle['y'] += particle['speed']
            particle['rotation'] += 0.2
            
            # Reposiciona partículas que saem da tela
            if particle['y'] > HEIGHT:
                particle['y'] = -50
                particle['x'] = random.randint(0, WIDTH)
                particle['symbol'] = random.choice(["∫", "∂", "∑", "√", "∞", "d/dx", "f'(x)", "∇", "∆", "∏"])

    def run(self):
        """Executa o loop do menu"""
        while self.running:
            self.time += 0.01
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Pressione Enter para iniciar
                        return "start"
                    elif event.key == pygame.K_ESCAPE:  # Pressione Esc para sair
                        return "quit"

            # Atualiza partículas
            self.update_snow_particles()
            self.update_math_particles()
            
            # Renderiza o menu
            self._draw_background()
            self._draw_menu()
            self._draw_car()
            self._draw_particles()
            pygame.display.flip()

    def _draw_background(self):
        """Desenha o fundo com gradiente mais contrastante"""
        # Define cores mais contrastantes para o gradiente
        top_color = (20, 30, 60)  # Azul escuro no topo
        bottom_color = (80, 10, 120)  # Roxo escuro na base
        
        # Cria um gradiente de fundo
        for y in range(0, HEIGHT, 2):
            # Calcula a cor do gradiente
            ratio = y / HEIGHT
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            color = (r, g, b)
            
            # Desenha uma linha horizontal com a cor calculada
            pygame.draw.line(self.screen, color, (0, y), (WIDTH, y), 2)
            
        # Adiciona um efeito de "estrelas" no fundo para melhorar o visual
        for _ in range(50):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.uniform(0.5, 2)
            brightness = random.randint(180, 255)
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (x, y), size)

    def _draw_menu(self):
        """Desenha o menu na tela com melhor contraste e elementos visuais"""
        # Adiciona um painel semi-transparente para o título para melhorar o contraste
        title_panel = pygame.Surface((WIDTH - 100, 120), pygame.SRCALPHA)
        title_panel.fill((0, 0, 0, 100))  # Preto semi-transparente
        self.screen.blit(title_panel, (50, 60))
        
        # Título do jogo com efeito de brilho
        title_font = self.fonts['title']
        # Sombra do título para melhorar legibilidade
        shadow_surface = title_font.render("Derivative Dash", True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(WIDTH//2 + 2, 102))
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Título com cor brilhante
        text_surface = title_font.render("Derivative Dash", True, (255, 255, 100))  # Amarelo brilhante
        text_rect = text_surface.get_rect(center=(WIDTH//2, 100))
        self.screen.blit(text_surface, text_rect)
        
        # Subtítulo com cor mais contrastante
        subtitle_font = self.fonts['medium']
        subtitle_surface = subtitle_font.render("Um jogo educacional sobre cálculo diferencial", True, (180, 255, 255))  # Ciano mais claro
        subtitle_rect = subtitle_surface.get_rect(center=(WIDTH//2, 150))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Painel para instruções
        instruction_panel = pygame.Surface((WIDTH - 200, 100), pygame.SRCALPHA)
        instruction_panel.fill((0, 0, 0, 120))  # Preto semi-transparente
        self.screen.blit(instruction_panel, (100, HEIGHT - 130))
        
        # Instruções com cores mais vibrantes
        instruction_font = self.fonts['medium']
        instruction1 = instruction_font.render("Pressione ENTER para iniciar", True, (255, 255, 0))  # Amarelo brilhante
        instruction2 = instruction_font.render("Pressione ESC para sair", True, (255, 150, 0))  # Laranja brilhante
        
        # Posiciona as instruções
        instr1_rect = instruction1.get_rect(center=(WIDTH//2, HEIGHT - 100))
        instr2_rect = instruction2.get_rect(center=(WIDTH//2, HEIGHT - 60))
        
        # Adiciona um efeito pulsante às instruções
        pulse = (math.sin(self.time * 3) + 1) * 0.5  # Valor entre 0 e 1
        instr1_scale = 1.0 + pulse * 0.05
        instr2_scale = 1.0 + pulse * 0.03
        
        # Redimensiona as instruções com o efeito pulsante
        instr1_scaled = pygame.transform.scale(instruction1, 
                                              (int(instruction1.get_width() * instr1_scale), 
                                               int(instruction1.get_height() * instr1_scale)))
        instr2_scaled = pygame.transform.scale(instruction2, 
                                              (int(instruction2.get_width() * instr2_scale), 
                                               int(instruction2.get_height() * instr2_scale)))
        
        # Atualiza os retângulos para as novas dimensões
        instr1_rect = instr1_scaled.get_rect(center=(WIDTH//2, HEIGHT - 100))
        instr2_rect = instr2_scaled.get_rect(center=(WIDTH//2, HEIGHT - 60))
        
        self.screen.blit(instr1_scaled, instr1_rect)
        self.screen.blit(instr2_scaled, instr2_rect)
        
        # Desenha linhas decorativas com gradiente
        for i in range(30):
            alpha = 255 - i * 8
            if alpha < 0:
                alpha = 0
            color = (255, 255, 255, alpha)
            pygame.draw.line(self.screen, color, 
                            (WIDTH//4 - i, HEIGHT//2 - i), 
                            (3*WIDTH//4 + i, HEIGHT//2 - i), 
                            1)

    def _draw_car(self):
        """Desenha o carro no menu com perspectiva corrigida"""
        # Faz o carro "flutuar" com um movimento suave
        self.car.y = HEIGHT - 150 + math.sin(self.time) * 5
        
        # Cria uma nova instância do carro especificamente para o menu
        # para garantir que ele esteja na orientação correta
        menu_car = self.car._create_surface(BLUE)
        
        # Adiciona um efeito de rotação suave para dar mais dinamismo
        angle = math.sin(self.time * 0.5) * 5  # Rotação suave entre -5 e 5 graus
        rotated_car = pygame.transform.rotate(menu_car, angle)
        
        # Posiciona o carro
        car_rect = rotated_car.get_rect(center=(WIDTH//2, self.car.y))
        
        # Adiciona um efeito de brilho ao redor do carro
        glow_size = 20
        glow_surface = pygame.Surface((rotated_car.get_width() + glow_size*2, 
                                      rotated_car.get_height() + glow_size*2), 
                                     pygame.SRCALPHA)
        
        # Desenha o brilho com gradiente
        for i in range(glow_size, 0, -1):
            alpha = 5 + (glow_size - i) * 2
            if alpha > 60:
                alpha = 60
            pygame.draw.rect(glow_surface, 
                            (100, 150, 255, alpha), 
                            (glow_size-i, glow_size-i, 
                             rotated_car.get_width()+i*2, 
                             rotated_car.get_height()+i*2), 
                            1)
        
        # Posiciona e desenha o brilho
        glow_rect = glow_surface.get_rect(center=car_rect.center)
        self.screen.blit(glow_surface, glow_rect)
        
        # Desenha o carro
        self.screen.blit(rotated_car, car_rect)
        
        # Adiciona um efeito de sombra mais realista
        shadow_width = rotated_car.get_width() - 10
        shadow_height = 15
        shadow = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
        
        # Cria uma sombra com gradiente para parecer mais realista
        for i in range(shadow_height):
            alpha = 100 - (i * 5)
            if alpha < 0:
                alpha = 0
            pygame.draw.ellipse(shadow, 
                               (0, 0, 0, alpha), 
                               (i//2, i, shadow_width - i, shadow_height - i*2))
        
        # Posiciona a sombra sob o carro
        shadow_rect = shadow.get_rect(center=(car_rect.centerx, car_rect.bottom + 5))
        self.screen.blit(shadow, shadow_rect)
        
        # Adiciona um efeito de reflexo sob o carro
        reflection_height = rotated_car.get_height() // 2
        reflection = pygame.transform.flip(rotated_car, False, True)
        reflection = pygame.transform.scale(reflection, 
                                           (rotated_car.get_width(), reflection_height))
        
        # Adiciona transparência ao reflexo
        for y in range(reflection_height):
            for x in range(reflection.get_width()):
                try:
                    r, g, b, a = reflection.get_at((x, y))
                    alpha = max(0, 70 - y)  # Diminui a opacidade conforme se afasta do carro
                    reflection.set_at((x, y), (r, g, b, alpha))
                except:
                    pass  # Ignora pixels fora dos limites
        
        # Desenha o reflexo
        reflection_rect = reflection.get_rect(midtop=(car_rect.centerx, car_rect.bottom + 2))
        self.screen.blit(reflection, reflection_rect)

    def _draw_particles(self):
        """Desenha as partículas (neve e cálculos) com melhor contraste"""
        # Desenha partículas de neve com efeito de brilho
        for particle in self.snow_particles:
            # Desenha um brilho ao redor da partícula
            glow_size = particle['size'] * 2
            pygame.draw.circle(
                self.screen, 
                (200, 200, 255, 50),  # Cor do brilho
                (int(particle['x']), int(particle['y'])), 
                int(glow_size)
            )
            
            # Desenha a partícula principal com cor mais brilhante
            bright_color = (255, 255, 255)  # Branco puro para melhor contraste
            pygame.draw.circle(
                self.screen, 
                bright_color, 
                (int(particle['x']), int(particle['y'])), 
                int(particle['size'])
            )
        
        # Desenha partículas de cálculos com efeito de brilho
        for particle in self.math_particles:
            # Cores mais vibrantes para os símbolos matemáticos
            bright_colors = [
                (255, 220, 100),  # Amarelo brilhante
                (100, 255, 255),  # Ciano brilhante
                (255, 150, 150),  # Rosa claro
                (150, 255, 150),  # Verde claro
                (200, 150, 255)   # Roxo claro
            ]
            
            # Escolhe uma cor baseada na posição da partícula para variedade
            color_index = int(particle['x'] + particle['y']) % len(bright_colors)
            bright_color = bright_colors[color_index]
            
            # Cria o texto com a nova cor
            font = pygame.font.SysFont("Arial", particle['size'])
            
            # Adiciona uma sombra para melhorar a legibilidade
            shadow_text = font.render(particle['symbol'], True, (0, 0, 0))
            shadow_rect = shadow_text.get_rect(center=(particle['x'] + 2, particle['y'] + 2))
            rotated_shadow = pygame.transform.rotate(shadow_text, particle['rotation'])
            shadow_rect = rotated_shadow.get_rect(center=shadow_rect.center)
            
            # Desenha a sombra com transparência
            shadow_surface = pygame.Surface(rotated_shadow.get_size(), pygame.SRCALPHA)
            shadow_surface.blit(rotated_shadow, (0, 0))
            shadow_surface.set_alpha(100)
            self.screen.blit(shadow_surface, shadow_rect)
            
            # Desenha o texto principal
            text = font.render(particle['symbol'], True, bright_color)
            text_rect = text.get_rect(center=(particle['x'], particle['y']))
            
            # Rotaciona o texto
            rotated_text = pygame.transform.rotate(text, particle['rotation'])
            rotated_rect = rotated_text.get_rect(center=text_rect.center)
            
            # Adiciona um efeito de pulsação
            pulse = (math.sin(self.time * 2 + particle['x'] * 0.01) + 1) * 0.5  # Valor entre 0 e 1
            alpha = int(150 + pulse * 105)  # Varia entre 150 e 255
            
            # Aplica o alpha
            rotated_text.set_alpha(alpha)
            
            self.screen.blit(rotated_text, rotated_rect)
