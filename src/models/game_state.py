import pygame
from src.models.car import Car
from src.models.track import Track
from src.models.functions import get_function, check_derivative_answer

class GameState:
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Reinicia o estado do jogo"""
        # Carrega a função atual
        function_data = get_function(0)
        
        # Inicializa a pista
        self.track = Track(function_data)
        
        # Inicializa o carro
        start_x = self.track.range[0] + 50
        self.car = Car(x=start_x)
        
        # Configurações da câmera
        self.camera_x = 0
        self.camera_y = self.track.get_y_at(start_x) - 300  # HEIGHT // 2
        
        # Estado do jogo
        self.input_mode = False
        self.input_text = ''
        self.message = ''
        self.message_time = 0
        self.score = 0
        self.game_over = False
        self.victory = False
        
        # Checkpoints
        self.checkpoints_passed = 0
        self.next_checkpoint = self.track.get_checkpoint_position(0)
        self.waiting_at_checkpoint = False
        
    def update(self):
        """Atualiza o estado do jogo"""
        if not self.game_over and not self.waiting_at_checkpoint:
            # Atualiza a posição do carro
            self.car.update_position(self.track.get_y_at)
            
            # Atualiza a câmera
            self.update_camera()
            
            # Verifica checkpoints
            self.check_checkpoint()
            
            # Verifica fim da pista
            self.check_end_of_track()
            
    def update_camera(self):
        """Atualiza a posição da câmera para seguir o carro"""
        self.camera_x = max(0, self.car.x - 333)  # WIDTH // 3
        self.camera_y = self.car.y - 300  # HEIGHT // 2
        
    def check_checkpoint(self):
        """Verifica se o carro chegou a um checkpoint"""
        if self.car.x >= self.next_checkpoint - 10 and not self.input_mode:
            self.car.speed = 0
            self.waiting_at_checkpoint = True
            self.input_mode = True
            self.message = f"Qual a derivada em x ≈ {int(self.next_checkpoint)}?"
            self.message_time = pygame.time.get_ticks()
            
    def check_end_of_track(self):
        """Verifica se o carro chegou ao fim da pista"""
        if self.track.is_end_of_track(self.car.x):
            self.car.x = self.track.range[1] - 50
            self.car.speed = 0
            
            if self.checkpoints_passed == self.track.total_checkpoints:
                self.victory = True
                self.message = f"🏁 VITÓRIA! Pontuação: {self.score}"
            else:
                self.message = "Fim da pista! Você não completou todos os checkpoints!"
                
            self.game_over = True
            
    def check_answer(self):
        """Verifica a resposta do usuário para a derivada no checkpoint"""
        real_slope = self.track.get_slope_at(self.car.x)
        
        if check_derivative_answer(self.input_text, real_slope):
            self.message = "✓ Correto! Continue!"
            self.car.speed = 2.0
            self.score += 100
            self.waiting_at_checkpoint = False
            self.input_mode = False
            self.checkpoints_passed += 1
            
            if self.checkpoints_passed < self.track.total_checkpoints:
                self.next_checkpoint = self.track.get_checkpoint_position(self.checkpoints_passed)
            else:
                self.next_checkpoint = self.track.range[1]
        else:
            self.message = "✗ Errado! Você bateu!"
            self.car.set_crashed()
            self.game_over = True
            
        self.input_text = ''
        self.message_time = pygame.time.get_ticks()