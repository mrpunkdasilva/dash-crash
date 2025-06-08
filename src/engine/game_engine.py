import pygame
import sys
from config.settings import WIDTH, HEIGHT, FPS, init_fonts
from src.models.game_state import GameState
from src.controllers.input_handler import InputHandler
from src.views.renderer import Renderer
from src.views.menu import Menu

class GameEngine:
    def __init__(self):
        """Inicializa o motor do jogo"""
        pygame.init()
        
        # Configuração da tela
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Derivative Dash - Cálculo 2")
        
        # Inicialização de componentes
        self.fonts = init_fonts()
        self.game_state = GameState()
        self.input_handler = InputHandler(self.game_state)
        self.renderer = Renderer(self.screen, self.fonts)
        self.menu = Menu(self.screen, self.fonts)
        
        # Controle de tempo
        self.clock = pygame.time.Clock()
        
        # Estado do jogo
        self.game_running = False
        
    def run(self):
        """Loop principal do jogo"""
        # Mostra o menu inicial
        menu_action = self.menu.run()
        
        if menu_action == "quit":
            pygame.quit()
            sys.exit()
            
        # Inicia o jogo
        self.game_running = True
        
        while self.game_running:
            # Processa entrada
            self.input_handler.handle_events()
            
            # Verifica se o usuário quer voltar ao menu
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] and self.game_state.game_over:
                # Reinicia o jogo e volta ao menu
                self.game_state.reset()
                menu_action = self.menu.run()
                
                if menu_action == "quit":
                    pygame.quit()
                    sys.exit()
                elif menu_action == "start":
                    continue
            
            # Atualiza estado do jogo
            self.game_state.update()
            
            # Renderiza
            self._render()
            
            # Controle de FPS
            self.clock.tick(FPS)
            
    def _render(self):
        """Renderiza o jogo com efeitos visuais melhorados"""
        # Limpa a tela com efeito de gradiente e partículas
        self.renderer.clear_screen()
        
        # Desenha a pista com efeitos visuais
        self.renderer.draw_track(
            self.game_state.track, 
            self.game_state.camera_x, 
            self.game_state.camera_y
        )
        
        # Desenha os checkpoints com efeitos visuais
        self.renderer.draw_checkpoints(
            self.game_state.track,
            self.game_state.checkpoints_passed,
            self.game_state.camera_x,
            self.game_state.camera_y
        )
        
        # Desenha o carro com efeitos visuais (rastro, partículas, etc.)
        self.renderer.draw_car(
            self.game_state.car,
            self.game_state.track,
            self.game_state.camera_x,
            self.game_state.camera_y
        )
        
        # Desenha painel de informações
        self.renderer.draw_info(self.game_state.track, self.game_state)
        
        # Desenha mensagens com efeitos visuais
        self.renderer.draw_message(
            self.game_state.message,
            self.game_state.game_over,
            self.game_state.victory,
            self.game_state.message_time
        )
        
        # Desenha caixa de entrada se necessário
        if self.game_state.input_mode and not self.game_state.game_over:
            self.renderer.draw_input_box(
                self.game_state.input_text,
                self.game_state.next_checkpoint
            )
            
        # Desenha tela de fim de jogo se necessário
        if self.game_state.game_over:
            self.renderer.draw_game_over(self.game_state)
            
        # Atualiza a tela
        pygame.display.flip()