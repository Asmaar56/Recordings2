import pygame
from bullet import Bullet
from typing import Tuple


class Player(pygame.sprite.Sprite):  # create player class
    def __init__(self,
                 image: pygame.Surface,
                 bullet_image: pygame.Surface,
                 position: Tuple[int, int],
                 all_sprites_group):  # takes image, position and sprite group as parameter

        # inherit sprite group
        super().__init__(all_sprites_group)

        self.all_sprites_group = all_sprites_group # create sprite group variable

        # image of player gets copied, so it is not continuously loaded
        self.image = image
        self.current_image = self.image.copy()
        self.image_scale = 0.5  # size of image

        # position variables
        self.position = pygame.math.Vector2(position[0], position[1])  # set position using parameter
        self.rect = self.image.get_rect()  # set player rect to the image's rect
        self.rect.center = (int(self.position.x), int(self.position.y))  # set centre using self.position
        self.view_pos_rect = self.rect.copy()  # make a copy of the rect, so it can be used for camera

        # movement variables
        self.speed = 5
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False

        # mouse rotation variables
        self.rotation_speed = 100.0
        self.current_rotation = 0.0

        # shooting attributes
        self.shooting = False
        self.bullet_image = bullet_image
        self.fire_rate = 1.0
        self.fire_timer = 2.0
        self.ready_to_fire = True

    # not in use anymore
    def movement(self, time_delta):  # this is where player movement is processed
        keys = pygame.key.get_pressed()  # get all key presses
        if keys[pygame.K_a]:  # if key is pressed
            self.move_left = True
            self.move_right = False
            self.position.x -= self.speed
        if keys[pygame.K_d]:  # if key is pressed
            self.move_left = True
            self.move_right = False
            self.position.x += self.speed
        if keys[pygame.K_w]:  # if key is pressed
            self.move_up = True
            self.move_down = False
            self.position.y -= self.speed
        if keys[pygame.K_s]:  # if key is pressed
            self.move_up = False
            self.move_down = True
            self.position.y += self.speed

        # find how much the mouse has moved relative to its last position
        relative_mouse_x, relative_mouse_y = pygame.mouse.get_rel()
        self.current_rotation = self.current_rotation - (relative_mouse_x * time_delta * self.rotation_speed)

        if self.shooting and self.ready_to_fire:
            self.shoot()
            self.ready_to_fire = False
            self.fire_timer = 0.0

    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:  # if key is pressed
            if event.key == pygame.K_a:
                self.move_left = True
            if event.key == pygame.K_d:
                self.move_right = True
            if event.key == pygame.K_w:
                self.move_up = True
            if event.key == pygame.K_s:
                self.move_down = True
            if event.key == pygame.K_f:
                self.shooting = True

        if event.type == pygame.KEYUP:  # if key is unpressed
            if event.key == pygame.K_a:
                self.move_left = False
            if event.key == pygame.K_d:
                self.move_right = False
            if event.key == pygame.K_w:
                self.move_up = False
            if event.key == pygame.K_s:
                self.move_down = False
            if event.key == pygame.K_f:
                self.shooting = False

    def update(self, time_delta, camera):  # update takes time since last frame as parameter

        if self.fire_timer >= self.fire_rate:
            self.ready_to_fire = True
        else:
            self.fire_timer += time_delta

        # find how much the mouse has moved relative to its last position
        relative_mouse_x, relative_mouse_y = pygame.mouse.get_rel()
        self.current_rotation = self.current_rotation - (relative_mouse_x * time_delta * self.rotation_speed)

        # rotate the image of the player when the mouse is moved
        self.image = pygame.transform.rotozoom(self.current_image,
                                               self.current_rotation,
                                               self.image_scale)
        self.rect.size = self.image.get_size()  # resize the image in case it has changed size
        self.rect.center = (int(self.position.x), int(self.position.y))  # recenter the image incase it has shifted
        self.view_pos_rect.size = self.rect.size
        self.view_pos_rect.centerx = self.rect.centerx - camera.viewport_rect.left
        self.view_pos_rect.centery = self.rect.centery - camera.viewport_rect.top
        self.rect.center = (int(self.view_pos_rect.centerx), int(self.view_pos_rect.centery))

        # player movement updating
        if self.move_left:
            self.position.x -= self.speed
        if self.move_right:
            self.position.x += self.speed
        if self.move_up:
            self.position.y -= self.speed
        if self.move_down:
            self.position.y += self.speed

        if self.shooting and self.ready_to_fire:
            self.shoot()
            self.ready_to_fire = False
            self.fire_timer = 0.0

    def shoot(self):
        Bullet(bullet_image=self.bullet_image,
               start_position=self.rect.center,
               direction_vector=pygame.Vector2(0.0, -1.0),
               owner='player',
               all_sprites_group=self.all_sprites_group)
