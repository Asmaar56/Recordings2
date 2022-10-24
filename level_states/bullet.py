import pygame
from pygame import Rect

# sets the data type of something to a tuple
# so python doesn't get confused and crashes
from typing import Tuple


class Bullet:
    def __init__(self, bullet_texture,
                 position: Tuple[int, int],
                 direction):  # type hint: Tuple, so python doesnt crash

        self.original_image = bullet_texture
        self.image: pygame.Surface = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.image_scale = 0.05

        # set position to whatever parameter was sent in
        self.position = pygame.Vector2(position[0], position[1])  # spawn location for the player
        self.direction = direction
        self.speed = 300.0  # player speed (in pixels)
        self.pos_rect = Rect(0, 0, 50, 38)  # pygame rect for the asteroid, scaled at the asteroid image size
        self.pos_rect.center = (int(self.position.x), int(self.position.y))

        upward_facing_vector = pygame.Vector2(0.0, -1.0)
        self.current_rotation = -upward_facing_vector.angle_to(self.direction) - 90

        self.view_pos_rect = self.pos_rect.copy()

    def update(self, dt, camera):  # import camera so you can edit the viewport

        self.rect.size = self.image.get_size()  # resize the image in case it has changed size
        move_vector = self.direction.copy()
        move_vector.scale_to_length(self.speed * dt)
        self.position += move_vector

        self.rect.center = self.position  # update image position

        # rotate image
        self.current_rotation += 20.0 * dt * 0
        # rotate the image of the player when the mouse is moved
        self.image = pygame.transform.rotozoom(self.original_image,
                                               self.current_rotation,
                                               self.image_scale)

        # update image position with camera
        bullet_view_pos = (self.position.x - camera.viewport_rect.left,
                           self.position.y - camera.viewport_rect.top)
        self.view_pos_rect.center = bullet_view_pos


    def draw(self, window_surface):
        # draw the image with the camera's position
        window_surface.blit(self.image, self.view_pos_rect)
