class Track:
    def __init__(self, function_data):
        self.function = function_data["f"]
        self.derivative = function_data["df"]
        self.name = function_data["name"]
        self.formula = function_data["formula"]
        self.range = function_data["range"]
        self.total_checkpoints = function_data["checkpoints"]
        self.track_length = self.range[1] - self.range[0]
        
        # Calcular posições dos checkpoints
        self.checkpoint_positions = self._calculate_checkpoint_positions()
        
    def _calculate_checkpoint_positions(self):
        """Calcula as posições dos checkpoints ao longo da pista"""
        spacing = self.track_length / (self.total_checkpoints + 1)
        return [self.range[0] + (i+1) * spacing for i in range(self.total_checkpoints)]
        
    def get_y_at(self, x):
        """Retorna a altura da pista em um ponto x"""
        return self.function(x)
        
    def get_slope_at(self, x):
        """Retorna a inclinação da pista em um ponto x"""
        return self.derivative(x)
        
    def get_checkpoint_position(self, index):
        """Retorna a posição do checkpoint pelo índice"""
        if 0 <= index < len(self.checkpoint_positions):
            return self.checkpoint_positions[index]
        return None
        
    def is_end_of_track(self, x, margin=50):
        """Verifica se o ponto x está próximo do fim da pista"""
        return x >= self.range[1] - margin