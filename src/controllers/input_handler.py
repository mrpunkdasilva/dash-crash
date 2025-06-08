import pygame
import sys

class InputHandler:
    def __init__(self, game_state):
        self.game_state = game_state
        
    def handle_events(self):
        """Processa todos os eventos de entrada"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            self._handle_keyboard_input(event)
                
        self._check_special_keys()
                
    def _handle_keyboard_input(self, event):
        """Processa entrada de teclado para o modo de entrada de texto"""
        if not self.game_state.game_over and self.game_state.input_mode:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_state.check_answer()
                elif event.key == pygame.K_BACKSPACE:
                    self.game_state.input_text = self.game_state.input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    # Cancela o modo de entrada
                    self.game_state.input_mode = False
                    self.game_state.input_text = ''
                    self.game_state.message = "Entrada cancelada"
                    self.game_state.message_time = pygame.time.get_ticks()
                elif event.unicode.isprintable():
                    # Limita o tamanho da entrada para evitar overflow
                    if len(self.game_state.input_text) < 10:
                        # Aceita apenas números, ponto e sinal de menos
                        if event.unicode in "0123456789.-":
                            self.game_state.input_text += event.unicode
                    
    def _check_special_keys(self):
        """Verifica teclas especiais"""
        keys = pygame.key.get_pressed()
        
        # Tecla de reinício
        if self.game_state.game_over and keys[pygame.K_r]:
            self.game_state.reset()
            
        # Tecla para aumentar velocidade (quando não estiver em checkpoint)
        if not self.game_state.game_over and not self.game_state.input_mode:
            if keys[pygame.K_RIGHT] or keys[pygame.K_UP]:
                self.game_state.car.speed = min(self.game_state.car.max_speed, self.game_state.car.speed + 0.1)
            elif keys[pygame.K_LEFT] or keys[pygame.K_DOWN]:
                self.game_state.car.speed = max(1.0, self.game_state.car.speed - 0.1)