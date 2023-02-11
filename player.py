import pygame
from level_states.bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self,
                 player_texture,
                 world_bounds,
                 window_surface,
                 player_shots_group: pygame.sprite.Group,
                 player_collision_group: pygame.sprite.Group,
                 all_sprites_group: pygame.sprite.Group,
                 enemy_group: pygame.sprite.Group):

        super().__init__(all_sprites_group)
        self.all_sprites_group = all_sprites_group
        self.player_shots_group = player_shots_group
        self.player_collision_group = player_collision_group
        self.enemy_group = enemy_group

        # initialise parameters
        self.world_bounds = world_bounds
        self.window_surface = window_surface
        self.original_image = player_texture
        # make a copy of the player's image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()  # set rect to have same boundaries as image
        self.image_scale = 0.5  # resize the image

        self.position = pygame.Vector2(500.0, 400.0)  # spawn location for the player
        self.rect.center = (int(self.position.x), int(self.position.y))
        self.view_pos_rect = self.rect.copy()  # set dimensions to pos rect dimensions
        self.world_facing_vector = pygame.Vector2(0.0, -1.0)  # vertically upwards for rotation

        self.speed = 300.0  # player speed (in pixels)
        self.move_up = False  # is movement key pressed?
        self.move_down = False

        self.rotate_left = False
        self.rotate_right = False
        self.current_rotation = 0.0

        # shooting variables
        self.shooting = False  # has shooting button been pressed?
        self.ready_to_shoot = False
        self.bullet_texture = pygame.image.load('level_states/game_images/laser2.png')  # load in bullet image
        self.bullet_list = []  # contains all bullets fired
        self.shooting_fire_rate = 1.0  # time between bullet creation
        self.shooting_fire_timer = 0.0  # counter since last bullet creation

        self.coins_collected = 0
        self.enemies_killed = 0

    def process_events(self, event):
        # inputs are handled here
        if event.type == pygame.KEYDOWN:  # is key pressed?
            if event.key == pygame.K_w:
                self.move_up = True
            if event.key == pygame.K_s:
                self.move_down = True
            if event.key == pygame.K_f:
                self.shooting = True

        if event.type == pygame.KEYUP:  # is key unpressed?
            if event.key == pygame.K_w:
                self.move_up = False
            if event.key == pygame.K_s:
                self.move_down = False
            if event.key == pygame.K_f:
                self.shooting = False

    def update(self, time_delta, camera):
        if self.alive():
            # check if player touched coin
            player_coin_collisions = pygame.sprite.spritecollide(self,
                                                                 self.player_collision_group,
                                                                 False)
            player_enemy_collisions = pygame.sprite.spritecollide(self,
                                                                  self.enemy_group,
                                                                  False)
            # kill coin if the player touches it
            if player_coin_collisions:
                for coin in player_coin_collisions:
                    coin.kill()
                    self.coins_collected += 1
            if player_enemy_collisions:
                self.kill()

            self.rect.center = self.position

            # rotation needs mouse position relative to upwards facing vector
            mouse_screen_pos = pygame.mouse.get_pos()
            world_mouse_pos = pygame.Vector2(mouse_screen_pos[0]+camera.viewport_rect.left,
                                             mouse_screen_pos[1]+camera.viewport_rect.top)
            # recalculate facing vector
            self.world_facing_vector = (world_mouse_pos - self.position).normalize()
            # set current rotation to the angle to the vertical axis
            upward_facing_vector = pygame.Vector2(0.0, -1.0)
            self.current_rotation = -upward_facing_vector.angle_to(self.world_facing_vector)

            # rotate the image of the player when the mouse is moved
            self.image = pygame.transform.rotozoom(self.original_image,
                                                   self.current_rotation,
                                                   self.image_scale)  # resize the image

            # get resize the view pos rect as it changes during rotation
            self.view_pos_rect.size = self.image.get_size()

            # move the player
            if self.move_up:
                self.position += self.world_facing_vector * self.speed * time_delta
            if self.move_down:
                self.position -= self.world_facing_vector * self.speed * time_delta

            # update fire timer
            if self.shooting_fire_timer > self.shooting_fire_rate:
                self.ready_to_shoot = True
            else:
                self.shooting_fire_timer += time_delta

            # make a bullet
            if self.shooting and self.ready_to_shoot:
                self.create_bullet()

            # update bullets
            for bullet in self.bullet_list:
                if bullet.update(time_delta, camera):
                    self.enemies_killed += 1

            # checks to see if the player should stop moving
            player_view_pos = (self.position.x - camera.viewport_rect.left,
                               self.position.y - camera.viewport_rect.top)
            self.view_pos_rect.center = player_view_pos
        else:
            print('dead')
            return True

    # create a bullet
    def create_bullet(self):
        # set variables to False, so timer restarts
        self.shooting = False
        self.ready_to_shoot = False
        self.shooting_fire_timer = 0.0

        # update bullet position with the camera's position
        bullet_position = (int(self.position.x),
                           int(self.position.y))
        # make bullet and append it to the bullet list
        self.bullet_list.append(Bullet(bullet_texture=self.bullet_texture,
                                       position=bullet_position,
                                       direction=self.world_facing_vector,
                                       all_sprites_group=self.all_sprites_group,
                                       player_shots_group=self.player_shots_group))

    def draw(self, window_surface):
        window_surface.blit(self.image, self.view_pos_rect)

        # draw bullets
        for bullet in self.bullet_list:
            bullet.draw(self.window_surface)




'''
import pygame
from bullet import Bullet
from laser import LaserShot
from arrow import Asteroid
from typing import Tuple
from random import randint


class Player(pygame.sprite.Sprite):  # create player class
    def __init__(self,
                 image: pygame.Surface,
                 bullet_image: pygame.Surface,
                 position: Tuple[int, int],
                 all_sprites_group,
                 window_surface):  # takes image, position and sprite group as parameter

        # inherit sprite group
        super().__init__(all_sprites_group)

        self.all_sprites_group = all_sprites_group  # create sprite group variable

        self.window_surface = window_surface

        self.bullet_list = []

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
        for bullet in self.bullet_list:
            bullet.rect.center = (int(self.view_pos_rect.centerx), int(self.view_pos_rect.centery))

        # player movement updating
        if self.move_left:
            self.position.x -= self.speed

        if self.move_right:
            self.position.x += self.speed

        if self.move_up:
            self.position.y -= self.speed

        if self.move_down:
            self.position.y += self.speed


        # player firing updaing
        if self.fire_timer >= self.fire_rate:
            self.ready_to_fire = True
        else:
            self.fire_timer += time_delta

        if self.shooting and self.ready_to_fire:
            self.shoot()
            self.ready_to_fire = False
            self.fire_timer = 0.0

        for asteroid in self.bullet_list:
            asteroid.update(time_delta, camera)
            asteroid.draw(self.window_surface)
            print("ASTEROID:", asteroid.position)
            print('PLAYER:', self.position)

                LaserShot(shot_image=self.bullet_image,
                          start_position=self.rect.midtop,
                          direction_vector=pygame.Vector2(0.0, -1.0),
                          owner='player',
                          all_sprites_group=self.all_sprites_group)

    def shoot(self):

        # asteroid position
        asteroid_position = (200, 200)
        self.bullet_list.append(Asteroid(self.bullet_image, asteroid_position))
        '''
