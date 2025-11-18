import pygame
from random import randint

BLACK = (0, 0, 0)


class Ball(pygame.sprite.Sprite):
    """Ball sprite for Pong."""

    def __init__(self, color, width, height):
        super().__init__()

        # Create a surface and make black transparent
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the ball as a circle
        radius = min(width, height) // 2
        center = (width // 2, height // 2)
        pygame.draw.circle(self.image, color, center, radius)

        # For pixel-perfect collisions
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.velocity = [0, 0]  # will be set by the main game

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        """Reverse horizontal direction and randomize vertical a bit."""
        self.velocity[0] = -self.velocity[0]
        # Keep vertical speed modest
        self.velocity[1] = randint(-9, 9)

    def change_color(self, color):
        """Redraw the ball with a new color."""
        width, height = self.image.get_size()
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        radius = min(width, height) // 2
        center = (width // 2, height // 2)
        pygame.draw.circle(self.image, color, center, radius)
        self.mask = pygame.mask.from_surface(self.image)
