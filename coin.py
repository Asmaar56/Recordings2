from typing import Tuple
import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self,
                 coin_texture: pygame.Surface,
                 position: Tuple[int, int],
                 player_collision_group: pygame.sprite.Group,
                 all_sprites_group: pygame.sprite.Group):

        super().__init__(player_collision_group, all_sprites_group)

        # image variables
        self.original_image = coin_texture
        self.image: pygame.Surface = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.image_scale = 0.1

        # set position to whatever parameter was sent in
        self.position = pygame.Vector2(position[0], position[1])  # spawn location for the player

        # rotation variables
        self.current_rotation = 0
        # rotate the image of the player when the mouse is moved
        self.image = pygame.transform.rotozoom(self.original_image,
                                               self.current_rotation,
                                               self.image_scale)
        self.rect.size = self.image.get_size()  # resize the image in case it has changed size

        # create view pos rect
        self.rect.center = (int(self.position.x),
                            int(self.position.y))
        self.view_pos_rect = self.rect.copy()

    def update(self, time_delta, camera):  # import camera so you can edit the viewport
        if self.alive():
            self.rect.center = self.position  # update image position

            # update image position with camera
            coin_view_pos = (self.position.x - camera.viewport_rect.left,
                             self.position.y - camera.viewport_rect.top)
            self.view_pos_rect.center = coin_view_pos

    def draw(self, window_surface):
        # draw the image with the camera's position
        # if still alive
        if self.alive():
            window_surface.blit(self.image, self.view_pos_rect)

