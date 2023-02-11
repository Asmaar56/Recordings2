import pygame
from pygame import Rect

# sets the data type of something to a tuple
# so python doesn't get confused and crashes
from typing import Tuple


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_texture,
                 position: Tuple[int, int],
                 direction,
                 player_shots_group: pygame.sprite.Group,
                 all_sprites_group: pygame.sprite.Group):  # type hint: Tuple, so python doesn't crash

        super().__init__(player_shots_group, all_sprites_group)

        # image variables
        self.original_image = bullet_texture
        self.image: pygame.Surface = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.image_scale = 0.05

        # set position to whatever parameter was sent in
        self.position = pygame.Vector2(position[0], position[1])  # spawn location for the player

        self.speed = 800.0  # bullet speed (in pixels)

        # direction variables
        self.direction = direction
        upward_facing_vector = pygame.Vector2(0.0, -1.0)
        self.current_rotation = -upward_facing_vector.angle_to(self.direction) - 90

        # rotate the image of the player when the mouse is moved
        self.image = pygame.transform.rotozoom(self.original_image,
                                               self.current_rotation,
                                               self.image_scale)
        self.rect.size = self.image.get_size()  # resize the image in case it has changed size

        self.rect.center = (int(self.position.x),
                            int(self.position.y))
        self.view_pos_rect = self.rect.copy()

    def update(self, time_delta, camera):  # import camera so you can edit the viewport

        if self.alive():
            move_vector = self.direction.copy()
            move_vector.scale_to_length(self.speed * time_delta)
            self.position += move_vector  # move bullet

            self.rect.center = self.position  # update image position

            # update image position with camera
            bullet_view_pos = (self.position.x - camera.viewport_rect.left,
                               self.position.y - camera.viewport_rect.top)
            self.view_pos_rect.center = bullet_view_pos
        else:
            return True

    def draw(self, window_surface):
        # draw the image with the camera's position
        if self.alive():
            window_surface.blit(self.image, self.view_pos_rect)
