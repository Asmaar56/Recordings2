import pygame
from typing import Tuple

class Bullet():
    def __init__(self,
                 bullet_image,
                 start_position: Tuple[int, int],
                 direction_vector: pygame.math.Vector2,
                 owner: str,):

        self.image = bullet_image
        self.owner = owner

        self.position = pygame.math.Vector2(start_position[0], start_position[1])
        self.direction=direction_vector.normalize()
        self.speed = 400.0

        self.rect = self.image.get_rect()
        self.rect.center = (int(self.position.x), int(self.position.y))

    def update(self, time_delta: float):
        self.position += (self.direction * self.speed * time_delta)

        self.rect.center = (int(self.position.x), int(self.position.y))