import pygame


class Camera:
    def __init__(self, start_world_pos: pygame.Vector2,
                 viewport_rect: pygame.Rect,
                 world_bounds: pygame.Rect):
        self.position = start_world_pos  # camera pos is the player's pos
        self.viewport_rect = viewport_rect  # viewport is what the camera sees
        self.world_bounds = world_bounds  # camera boundaries

    #  updates the camera according to the viewport position and the world bounds
    def update(self, time_delta, player_position: pygame.Vector2):
        # set camera pos to player pos
        self.position.x = player_position.x
        self.position.y = player_position.y

        # set viewport to player pos
        self.viewport_rect.center = self.position

        if self.viewport_rect.left < self.world_bounds.left:
            self.viewport_rect.left = self.world_bounds.left

        if self.viewport_rect.right > self.world_bounds.right:
            self.viewport_rect.right = self.world_bounds.right

        if self.viewport_rect.top < self.world_bounds.top:
            self.viewport_rect.top = self.world_bounds.top

        if self.viewport_rect.bottom > self.world_bounds.bottom:
            self.viewport_rect.bottom = self.world_bounds.bottom


'''
import pygame


class Camera:
    def __init__(self, start_world_pos: pygame.Vector2, viewport_rect: pygame.Rect):
        self.position = start_world_pos
        self.viewport_rect = viewport_rect

    def update(self, dt, player_position: pygame.Vector2):
        self.position.x = player_position.x
        self.position.y = player_position.y

        self.viewport_rect.center = self.position
'''