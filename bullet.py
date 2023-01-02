import pygame
from pygame import Rect

from typing import Tuple

import random


class Bullet(pygame.sprite.Sprite):  # bullet is a sprite
    def __init__(self,
                 bullet_image: pygame.Surface,
                 position: Tuple[int, int],
                 direction_vectors: pygame.math.Vector2,
                 owner: str,
                 all_sprites_group: pygame.sprite.Group):
        super().__init__(all_sprites_group)

        self.owner = owner

        self.image = bullet_image
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()

        self.image_scale = 0.05
        self.current_rotation = -90

        # set position to whatever parameter was sent in
        self.position = pygame.Vector2(position[0], position[1])  # spawn location for the player
        self.direction = pygame.Vector2(random.random(), random.random()).normalize()
        self.speed = 20.0  # player speed (in pixels)
        self.pos_rect = Rect(0, 0, 50, 38)  # pygame rect for the asteroid, scaled at the asteroid image size
        self.pos_rect.center = (int(self.position.x), int(self.position.y))

        '''
        # bullet position variables
        self.position = pygame.math.Vector2(position[0], position[1])
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.position.x), int(self.position.y))
        self.view_pos_rect = self.rect.copy()  # make a copy of the rect, so it can be used for camera
        '''
        self.view_pos_rect = self.pos_rect.copy()


        # rotate the image of the player when the mouse is moved
        self.image = pygame.transform.rotozoom(self.original_image,
                                               self.current_rotation,
                                               self.image_scale)
        self.rect.size = self.image.get_size()


    def update(self, time_delta: float, camera):
        move_vector = self.direction.copy()
        move_vector.scale_to_length(self.speed * time_delta)
        self.position += move_vector

        self.rect.center = self.position  # update image position

        # rotate image
        self.current_rotation += 20.0 * time_delta
        self.image = pygame.transform.rotate(self.original_image, self.current_rotation)

        # update image position with camera
        asteroid_view_pos = (self.position.x - camera.viewport_rect.left,
                             self.position.y - camera.viewport_rect.top)
        self.view_pos_rect.center = asteroid_view_pos

    def draw(self, window_surface):

        window_surface.blit(self.image, self.view_pos_rect)