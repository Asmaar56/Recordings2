import pygame


class Camera:
    def __init__(self, start_world_pos: pygame.Vector2, viewport_rect: pygame.Rect):
        self.position = start_world_pos
        self.viewport_rect = viewport_rect

    def update(self, dt, player_position: pygame.Vector2):
        self.position.x = player_position.x
        self.position.y = player_position.y

        self.viewport_rect.center = self.position
