import pygame
import math
import random
from config.settings import (
    WIDTH, HEIGHT, BLACK, GRAY, GREEN, ORANGE, RED, BLUE, WHITE,
    UI_PRIMARY, UI_SECONDARY, UI_ACCENT, UI_TEXT, UI_WARNING, UI_DANGER, UI_SUCCESS,
    BG_LIGHT, BG_DARK, HIGHLIGHT_BLUE, HIGHLIGHT_GREEN, HIGHLIGHT_RED, HIGHLIGHT_YELLOW,
    LIGHT_GRAY, DARK_GRAY, CYAN, PURPLE
)

class Renderer:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.background_particles = []
        self.generate_background_particles(50)
        self.time = 0
        
    def generate_background_particles(self, count):
        """Gera partículas de fundo para efeito visual"""
        for _ in range(count):
            self.background_particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.uniform(1, 3),
                'speed': random.uniform(0.2, 1.0),
                'color': (
                    random.randint(200, 255),
                    random.randint(200, 255),
                    random.randint(200, 255),
                    random.randint(50, 150)
                )
            })
            
    def update_background_particles(self):
        """Atualiza as partículas de fundo"""
        self.time += 0.01
        
        for particle in self.background_particles:
            # Move as partículas lentamente
            particle['y'] += particle['speed']
            particle['x'] += math.sin(self.time + particle['y'] * 0.01) * 0.5
            
            # Reposiciona partículas que saem da tela
            if particle['y'] > HEIGHT:
                particle['y'] = 0
                particle['x'] = random.randint(0, WIDTH)
                
            if particle['x'] < 0:
                particle['x'] = WIDTH
            elif particle['x'] > WIDTH:
                particle['x'] = 0
        
    def clear_screen(self):
        """Limpa a tela usando o gradiente e estrelas do menu para consistência visual"""
        from src.views.backgrounds import draw_menu_background
        draw_menu_background(self.screen, self.time, stars_count=50)
        # (Opcional) Se quiser manter partículas de fundo do jogo, descomente abaixo:
        # self.update_background_particles()
        # for particle in self.background_particles:
        #     pygame.draw.circle(
        #         self.screen, 
        #         particle['color'], 
        #         (int(particle['x']), int(particle['y'])), 
        #         int(particle['size'])
        #     )
        
    def draw_track(self, track, camera_x, camera_y):
        """Desenha a pista com efeitos visuais melhorados"""
        # Desenha a pista principal com mais detalhes
        points = []
        step = max(1, track.track_length // 800)  # Aumenta a resolução da pista
        
        for x in range(track.range[0], track.range[1], step):
            y = track.get_y_at(x)
            screen_y = HEIGHT - (y - camera_y)
            points.append((x - camera_x, screen_y))
            
        if len(points) > 1:
            # Desenha a pista com efeito de sombra mais sutil
            shadow_points = [(p[0] + 3, p[1] + 3) for p in points]
            pygame.draw.lines(self.screen, (50, 50, 50, 100), False, shadow_points, 16)
            
            # Desenha o fundo da pista com gradiente
            track_color = (100, 100, 120)  # Cor base da pista
            pygame.draw.lines(self.screen, track_color, False, points, 14)
            
            # Desenha a linha central da pista
            pygame.draw.lines(self.screen, (180, 180, 180), False, points, 2)
            
            # Desenha as bordas da pista com destaque
            edge_color = (220, 220, 220)
            
            # Borda superior (paralela à pista)
            upper_edge_points = []
            for x, y in points:
                upper_edge_points.append((x, y - 7))
            pygame.draw.lines(self.screen, edge_color, False, upper_edge_points, 2)
            
            # Borda inferior (paralela à pista)
            lower_edge_points = []
            for x, y in points:
                lower_edge_points.append((x, y + 7))
            pygame.draw.lines(self.screen, edge_color, False, lower_edge_points, 2)
            
            # Desenha marcações na pista (mais frequentes e com cores alternadas)
            for i in range(0, len(points), 10):
                if i + 1 < len(points):
                    mid_x = (points[i][0] + points[i+1][0]) // 2
                    mid_y = (points[i][1] + points[i+1][1]) // 2
                    
                    # Alterna cores das marcações (usando cores já importadas)
                    mark_color = WHITE if i % 20 == 0 else (255, 255, 0)  # Amarelo
                    mark_size = 3 if i % 20 == 0 else 2
                    
                    pygame.draw.circle(self.screen, mark_color, (mid_x, mid_y), mark_size)
            
    def draw_checkpoints(self, track, checkpoints_passed, camera_x, camera_y):
        """Desenha os checkpoints com efeitos visuais melhorados"""
        for i, checkpoint_x in enumerate(track.checkpoint_positions):
            y = track.get_y_at(checkpoint_x)
            pos = (checkpoint_x - camera_x, HEIGHT - (y - camera_y))
            
            if -50 < pos[0] < WIDTH + 50:
                # Define cores e estilos com base no estado do checkpoint
                if i < checkpoints_passed:  # Checkpoint já passado
                    color = UI_SUCCESS
                    glow_color = HIGHLIGHT_GREEN
                    fill = 0
                    size = 12
                    pulse = 0
                elif i == checkpoints_passed:  # Próximo checkpoint
                    color = UI_WARNING
                    glow_color = HIGHLIGHT_YELLOW
                    fill = 0
                    size = 15
                    # Efeito de pulsação
                    pulse = math.sin(pygame.time.get_ticks() * 0.005) * 3
                else:  # Checkpoints futuros
                    color = UI_DANGER
                    glow_color = HIGHLIGHT_RED
                    fill = 2
                    size = 12
                    pulse = 0
                
                # Desenha o efeito de brilho
                pygame.draw.circle(self.screen, glow_color, pos, size + pulse, 0)
                
                # Desenha o checkpoint
                pygame.draw.circle(self.screen, color, pos, size, fill)
                
                # Adiciona número do checkpoint
                checkpoint_num = self.fonts["small"].render(str(i+1), True, WHITE)
                self.screen.blit(
                    checkpoint_num, 
                    (pos[0] - checkpoint_num.get_width()//2, 
                     pos[1] - checkpoint_num.get_height()//2)
                )
                
    def draw_car(self, car, track, camera_x, camera_y):
        """Desenha o carro e seus efeitos visuais"""
        # Desenha os efeitos do carro (rastro e partículas)
        car.draw_effects(self.screen, camera_x, camera_y, HEIGHT)
        
        # Desenha o carro
        car_y = track.get_y_at(car.x)
        slope = track.get_slope_at(car.x)
        rotated_car = car.get_rotated_surface(slope)
        
        # Adiciona uma sombra sutil sob o carro (mais transparente e menor)
        shadow_width = rotated_car.get_width() - 10
        shadow_height = 5
        shadow = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 60), (0, 0, shadow_width, shadow_height))
        
        # Posiciona a sombra sob o carro
        shadow_x = car.x - camera_x - shadow_width//2
        shadow_y = HEIGHT - (car_y - camera_y) + 5
        self.screen.blit(shadow, (shadow_x, shadow_y))
        
        # Desenha o carro
        self.screen.blit(
            rotated_car, 
            (car.x - camera_x - rotated_car.get_width()//2,
             HEIGHT - (car_y - camera_y) - rotated_car.get_height()//2)
        )
        
    def draw_info(self, track, game_state):
        """Desenha painel de informações do jogo"""
        # Cria um painel para as informações
        panel_width = 280
        panel_height = 150
        panel_x = 20
        panel_y = 20
        
        # Desenha o painel com transparência
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((UI_PRIMARY[0], UI_PRIMARY[1], UI_PRIMARY[2], 200))
        pygame.draw.rect(panel, UI_SECONDARY, (0, 0, panel_width, panel_height), 2, border_radius=10)
        
        # Adiciona um cabeçalho
        header = pygame.Surface((panel_width, 30), pygame.SRCALPHA)
        header.fill((UI_SECONDARY[0], UI_SECONDARY[1], UI_SECONDARY[2], 230))
        pygame.draw.rect(header, UI_ACCENT, (0, 0, panel_width, 30), 2, border_radius=10)
        panel.blit(header, (0, 0))
        
        # Título do painel
        title = self.fonts["medium"].render("INFORMAÇÕES", True, UI_TEXT)
        panel.blit(title, (panel_width//2 - title.get_width()//2, 5))
        
        # Informações do jogo
        info_text = [
            f"Função: {track.name}",
            f"Equação: {track.formula}",
            f"Velocidade: {game_state.car.speed:.1f} km/h",
            f"Checkpoints: {game_state.checkpoints_passed}/{track.total_checkpoints}",
            f"Pontuação: {game_state.score}",
        ]
        
        for i, text in enumerate(info_text):
            text_surface = self.fonts["small"].render(text, True, UI_TEXT)
            panel.blit(text_surface, (10, 35 + i * 22))
        
        # Desenha o painel na tela
        self.screen.blit(panel, (panel_x, panel_y))
        
        # Desenha um indicador de velocidade
        self._draw_speed_indicator(game_state.car.speed, game_state.car.max_speed, WIDTH - 150, 20)
            
    def _draw_speed_indicator(self, speed, max_speed, x, y):
        """Desenha um indicador visual de velocidade"""
        width = 120
        height = 30
        
        # Fundo do indicador
        pygame.draw.rect(self.screen, UI_PRIMARY, (x, y, width, height), border_radius=5)
        pygame.draw.rect(self.screen, UI_SECONDARY, (x, y, width, height), 2, border_radius=5)
        
        # Barra de velocidade
        speed_ratio = min(1.0, speed / max_speed)
        bar_width = int(width * speed_ratio)
        
        # Cor da barra baseada na velocidade
        if speed_ratio < 0.3:
            bar_color = GREEN
        elif speed_ratio < 0.7:
            bar_color = ORANGE
        else:
            bar_color = RED
            
        pygame.draw.rect(self.screen, bar_color, (x + 2, y + 2, bar_width - 4, height - 4), border_radius=5)
        
        # Texto da velocidade
        speed_text = self.fonts["small"].render(f"{speed:.1f} km/h", True, WHITE)
        self.screen.blit(speed_text, (x + width//2 - speed_text.get_width()//2, y + height//2 - speed_text.get_height()//2))
            
    def draw_message(self, message, game_over, victory, message_time):
        """Desenha mensagens para o jogador com efeitos visuais"""
        current_time = pygame.time.get_ticks()
        
        if current_time - message_time < 5000 or game_over:
            # Define a cor e o estilo com base no tipo de mensagem
            if "✓" in message or victory:
                msg_color = UI_SUCCESS
                bg_color = (0, 100, 0, 180)
                border_color = HIGHLIGHT_GREEN
            else:
                msg_color = UI_DANGER
                bg_color = (100, 0, 0, 180)
                border_color = HIGHLIGHT_RED
                
            # Cria uma caixa para a mensagem
            msg_surface = self.fonts["large"].render(message, True, WHITE)
            padding = 20
            box_width = msg_surface.get_width() + padding * 2
            box_height = msg_surface.get_height() + padding * 2
            
            # Posição da caixa
            box_x = WIDTH//2 - box_width//2
            box_y = 50
            
            # Desenha a caixa com transparência
            box = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            box.fill(bg_color)
            pygame.draw.rect(box, border_color, (0, 0, box_width, box_height), 3, border_radius=10)
            
            # Adiciona a mensagem à caixa
            box.blit(msg_surface, (padding, padding))
            
            # Efeito de pulsação se não for game over
            if not game_over:
                scale = 1.0 + math.sin(current_time * 0.01) * 0.05
                box = pygame.transform.scale(box, (int(box_width * scale), int(box_height * scale)))
            
            # Desenha a caixa na tela
            self.screen.blit(box, (WIDTH//2 - box.get_width()//2, box_y))
            
    def draw_input_box(self, input_text, next_checkpoint):
        """Desenha a caixa de entrada para a resposta do usuário com estilo melhorado"""
        # Cria um painel para a entrada
        panel_width = 400
        panel_height = 80
        panel_x = WIDTH//2 - panel_width//2
        panel_y = HEIGHT - panel_height - 20
        
        # Desenha o painel com transparência
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((UI_PRIMARY[0], UI_PRIMARY[1], UI_PRIMARY[2], 230))
        pygame.draw.rect(panel, UI_SECONDARY, (0, 0, panel_width, panel_height), 2, border_radius=10)
        
        # Título do painel
        title = self.fonts["medium"].render(f"Derivada em x ≈ {int(next_checkpoint)}", True, UI_TEXT)
        panel.blit(title, (panel_width//2 - title.get_width()//2, 10))
        
        # Caixa de entrada
        input_bg = pygame.Rect(20, 40, panel_width - 40, 30)
        pygame.draw.rect(panel, LIGHT_GRAY, input_bg, border_radius=5)
        pygame.draw.rect(panel, UI_ACCENT, input_bg, 2, border_radius=5)
        
        # Texto de entrada
        input_text_surface = self.fonts["medium"].render(input_text, True, BLACK)
        panel.blit(input_text_surface, (panel_width//2 - input_text_surface.get_width()//2, 45))
        
        # Cursor piscante
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = panel_width//2 + input_text_surface.get_width()//2 + 2
            pygame.draw.line(panel, BLACK, (cursor_x, 45), (cursor_x, 45 + input_text_surface.get_height()), 2)
        
        # Desenha o painel na tela
        self.screen.blit(panel, (panel_x, panel_y))
        
    def draw_game_over(self, game_state):
        """Desenha a tela de fim de jogo com efeitos visuais melhorados"""
        # Cria um overlay com transparência
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Painel principal
        panel_width = 500
        panel_height = 300
        panel_x = WIDTH//2 - panel_width//2
        panel_y = HEIGHT//2 - panel_height//2
        
        # Desenha o painel
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        
        if game_state.car.crashed:
            panel.fill((UI_DANGER[0], UI_DANGER[1], UI_DANGER[2], 200))
            border_color = HIGHLIGHT_RED
            title_text = "VOCÊ BATEU!"
            title_color = WHITE
        elif game_state.victory:
            panel.fill((UI_SUCCESS[0], UI_SUCCESS[1], UI_SUCCESS[2], 200))
            border_color = HIGHLIGHT_GREEN
            title_text = "VITÓRIA!"
            title_color = WHITE
        
        pygame.draw.rect(panel, border_color, (0, 0, panel_width, panel_height), 4, border_radius=15)
        
        # Título
        title = self.fonts["title"].render(title_text, True, title_color)
        panel.blit(title, (panel_width//2 - title.get_width()//2, 40))
        
        # Pontuação
        score_text = self.fonts["large"].render(f"Pontuação final: {game_state.score}", True, WHITE)
        panel.blit(score_text, (panel_width//2 - score_text.get_width()//2, 120))
        
        # Botão de reinício
        button_width = 300
        button_height = 50
        button_x = panel_width//2 - button_width//2
        button_y = 200
        
        pygame.draw.rect(panel, UI_SECONDARY, (button_x, button_y, button_width, button_height), border_radius=10)
        pygame.draw.rect(panel, WHITE, (button_x, button_y, button_width, button_height), 2, border_radius=10)
        
        restart_text = self.fonts["medium"].render("Pressione R para jogar novamente", True, WHITE)
        panel.blit(restart_text, (panel_width//2 - restart_text.get_width()//2, button_y + button_height//2 - restart_text.get_height()//2))
        
        # Desenha o painel na tela
        self.screen.blit(panel, (panel_x, panel_y))
        
        # Adiciona partículas decorativas
        for _ in range(2):
            particle = {
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.uniform(2, 5),
                'color': border_color
            }
            pygame.draw.circle(
                self.screen, 
                particle['color'], 
                (int(particle['x']), int(particle['y'])), 
                int(particle['size'])
            )