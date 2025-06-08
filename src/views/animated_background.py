import pygame
import random
import math
from config.settings import WIDTH, HEIGHT

class AnimatedBackground:
    def __init__(self, n_stars=50, n_particles=0):
        self.n_stars = n_stars
        self.n_particles = n_particles
        self.stars = []
        self.particles = []
        self._init_stars()
        if n_particles > 0:
            self._init_particles()

    def _init_stars(self):
        self.stars = []
        for _ in range(self.n_stars):
            star = {
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.uniform(0.5, 2.5),
                'base_brightness': random.randint(180, 255),
                'phase': random.uniform(0, math.pi*2),
                'speed': random.uniform(0.02, 0.08),
                'offset': random.uniform(-0.2, 0.2)
            }
            self.stars.append(star)

    def _init_particles(self):
        self.particles = []
        for _ in range(self.n_particles):
            particle = {
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.uniform(1, 3),
                'color': (
                    random.randint(100, 255),
                    random.randint(100, 255),
                    random.randint(100, 255),
                    random.randint(60, 120)
                ),
                'speed_x': random.uniform(-0.1, 0.1),
                'speed_y': random.uniform(0.05, 0.2)
            }
            self.particles.append(particle)

    def update(self, dt=1.0):
        # Move estrelas lentamente
        for star in self.stars:
            star['y'] += star['speed'] * dt
            star['x'] += star['offset'] * dt
            if star['y'] > HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, WIDTH)
            if star['x'] < 0:
                star['x'] = WIDTH
            elif star['x'] > WIDTH:
                star['x'] = 0
        # Move partículas (se houver)
        for p in self.particles:
            p['x'] += p['speed_x'] * dt
            p['y'] += p['speed_y'] * dt
            if p['y'] > HEIGHT:
                p['y'] = 0
                p['x'] = random.randint(0, WIDTH)
            if p['x'] < 0:
                p['x'] = WIDTH
            elif p['x'] > WIDTH:
                p['x'] = 0

    def draw(self, screen, time=0):
        # Gradiente de fundo
        top_color = (20, 30, 60)
        bottom_color = (80, 10, 120)
        for y in range(0, HEIGHT, 2):
            ratio = y / HEIGHT
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            color = (r, g, b)
            pygame.draw.line(screen, color, (0, y), (WIDTH, y), 2)
        # Estrelas animadas
        for star in self.stars:
            # Brilho pulsante
            pulse = (math.sin(time*1.5 + star['phase']) + 1) * 0.5
            brightness = int(star['base_brightness'] * (0.7 + 0.3 * pulse))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), int(star['size']))
        # Partículas coloridas (opcional)
        for p in self.particles:
            pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), int(p['size']))
